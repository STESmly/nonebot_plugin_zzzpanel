import json
import asyncio
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent,MessageSegment,Message,Bot
from pathlib import Path
from nonebot.params import CommandArg
from .intopng import get_avatar_list_png,get_avatar_info_png
from .utils import *

ZZZ_als = on_command("ZZZ图鉴")
ZZZ_uid = on_command("ZZZ绑定")
ZZZ_ld = on_command("ZZZ练度")
ZZZ_update_info = on_command("ZZZ更新数据")


@ZZZ_uid.handle()
async def _(event: GroupMessageEvent,bot:Bot):
    ticekt,uuid_d = await get_qr(event.user_id)
    data = await ZZZ_uid.send(MessageSegment.image(Path(f"{module_path}/qrcode/{event.user_id}.png"))+MessageSegment.at(event.user_id)+MessageSegment.text("请使用米游社扫码登录"))
    while True:
        record,status,cookies = await check_qr(ticekt,uuid_d)
        await asyncio.sleep(1)
        if status == "Confirmed":
            await ZZZ_uid.send(MessageSegment.at(event.user_id)+MessageSegment.text("扫码成功，正在获取游戏数据"))
            cookies = json.loads(cookies)
            await save_cookie(cookies,event.user_id)
            uid = await getuid(cookies)
            avatar_id_list = await get_avatar_id_list(uid,cookies)
            await save_avatar(avatar_id_list,event.user_id)
            await get_avatar_info_list(cookies,avatar_id_list,uid,event.user_id)
            await get_avatar_list_png(event.user_id)
            await ZZZ_uid.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id)+MessageSegment.at(event.user_id))
            break
        elif record == -3501:
            await ZZZ_uid.send(MessageSegment.at(event.user_id)+MessageSegment.text("扫码超时，请重新发送【ZZZ绑定】以获取二维码"))
            break
        elif record == -3505:
            await ZZZ_uid.send(MessageSegment.at(event.user_id)+MessageSegment.text("您已取消扫码，请重新发送【ZZZ绑定】以获取二维码"))
            break
    await bot.delete_msg(message_id=data["message_id"])

@ZZZ_als.handle()
async def _(event: GroupMessageEvent):
    if await check_cookie(event.user_id):
        await get_avatar_list_png(event.user_id)
        await ZZZ_als.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id))
    else:
        await ZZZ_als.send(MessageSegment.at(event.user_id) + MessageSegment.text("请先发送【ZZZ绑定】使用米游社扫码登录"))


@ZZZ_ld.handle()
async def _(event: GroupMessageEvent,args: Message = CommandArg()):
    if await check_cookie(event.user_id):
        args = args.extract_plain_text()
        tp,num = await check_avatar(event.user_id,args)
        if tp == True:
            await get_avatar_info_png(event.user_id,num)
            await ZZZ_ld.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id))
        else:
            await get_avatar_info_png(event.user_id,0)
            await ZZZ_ld.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id))
    else:
        await ZZZ_als.send(MessageSegment.at(event.user_id) + MessageSegment.text("请先发送【ZZZ绑定】使用米游社扫码登录"))

@ZZZ_update_info.handle()
async def _(event: GroupMessageEvent,args: Message = CommandArg()):
    if await check_cookie(event.user_id):
        cookies = await load_cookie(event.user_id)
        uid = await getuid(cookies)
        avatar_id_list = await get_avatar_id_list(uid,cookies)
        await save_avatar(avatar_id_list,event.user_id)
        if len(args)>0:
            if args == "图鉴":
                await ZZZ_ld.send(MessageSegment.at(event.user_id) + MessageSegment.text("更新成功，正在保存数据"))
                await get_avatar_list_png(event.user_id)
                await ZZZ_ld.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id))
            elif args == "练度":
                await get_avatar_info_list(cookies,avatar_id_list,uid,event.user_id)
                await ZZZ_ld.send(MessageSegment.at(event.user_id) + MessageSegment.text("更新成功，正在保存数据"))
            else:
                await ZZZ_ld.send(MessageSegment.at(event.user_id) + MessageSegment.text("参数错误"))
        else:
            await ZZZ_ld.send(MessageSegment.at(event.user_id) + MessageSegment.text("更新成功，正在保存数据"))
            await get_avatar_info_list(cookies,avatar_id_list,uid,event.user_id)
            await get_avatar_list_png(event.user_id)
            await ZZZ_ld.send(MessageSegment.image(Path(f"{module_path}/out/{event.user_id}.png"))+MessageSegment.at(event.user_id))
    else:
        await ZZZ_als.send(MessageSegment.at(event.user_id) + MessageSegment.text("请先发送【ZZZ绑定】使用米游社扫码登录"))