import asyncio
import json
import re
import httpx
import qrcode
import uuid
import json
import os
from pathlib import Path
from fuzzywuzzy import fuzz
from .config import Config
from nonebot import get_plugin_config
from nonebot import require
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store
plugin_config = get_plugin_config(Config)


module_path: Path = store.get_plugin_data_dir()
plugin_data_file: Path = store.get_plugin_data_file("filename")


async def create_qr(data,user_id):
    def generate_and_save_qr(data, user_id, module_path):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_path = f"{module_path}/qrcode/{user_id}.png"
        img.save(img_path)

    await asyncio.to_thread(generate_and_save_qr, data, user_id, module_path)

async def get_qr(user_id):
    uuid_d = uuid.uuid4()
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "x-rpc-app_id":"bll8iq97cem8",
        'x-rpc-device_fp': f'{plugin_config.x_rpc_device_fp}',
        "x-rpc-device_id":f"{uuid_d}"
    }
    creat_qr_url = "https://passport-api.miyoushe.com/account/ma-cn-passport/web/createQRLogin"
    async with httpx.AsyncClient() as client:
        r = await client.post(url=creat_qr_url, headers=headers)
        data = r.json()
        await create_qr(data["data"]['url'], user_id)
        return data["data"]["ticket"], uuid_d

async def check_qr(ticekt,uuid_d):
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "x-rpc-app_id":"bll8iq97cem8",
        'x-rpc-device_fp': f'{plugin_config.x_rpc_device_fp}',
        "x-rpc-device_id":f"{uuid_d}"
    }
    check_qr_url = "https://passport-api.miyoushe.com/account/ma-cn-passport/web/queryQRLoginStatus"
    async with httpx.AsyncClient() as client:
        r = await client.post(url=check_qr_url, headers=headers,json={"ticket": ticekt})
        data:dict = r.json()
        cookies_json = json.dumps(dict(r.cookies), indent=4)
        record = data["retcode"]
        status_data:dict = data.get("data", {})
        if status_data == None:
            status = None
        else:
            status = status_data.get("status", None)
        return record,status,cookies_json
    
async def getuid(cookies):
    headers = {
        'Host': 'api-takumi.mihoyo.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; 23113RKC6C Build/PQ3A.190605.06200901; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 miHoYoBBS/2.75.2',
        'Origin': 'https://act.mihoyo.com',
        'X-Requested-With': 'com.mihoyo.hyperion',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://act.mihoyo.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    params = {'game_biz': 'nap_cn',}
    async with httpx.AsyncClient() as client:
        r = await client.get('https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie',params=params,cookies=cookies,headers=headers)
        data = r.json()
        uid = data['data']['list'][0]['game_uid']
    return uid

async def get_avatar_id_list(uid, cookies):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ANP-AN00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36 miHoYoBBS/2.88.2',
            'x-rpc-device_fp': f'{plugin_config.x_rpc_device_fp}',
        }
        params = {'server': 'prod_gf_cn','role_id': uid,}
        async with httpx.AsyncClient() as client:
            r = await client.get('https://api-takumi-record.mihoyo.com/event/game_record_zzz/api/zzz/avatar/basic', params = params, headers = headers, cookies = cookies)
            res = r.json()
        avatar_id_list = res['data']['avatar_list']
        return avatar_id_list
    except:
        with open("avatar_id_list.json","r",encoding="utf-8") as f:
            avatar_id_list = json.load(f)
        return avatar_id_list

async def get_avater_info(cookies, aid, uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; ANP-AN00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36 miHoYoBBS/2.88.2',
        'x-rpc-device_fp': f'{plugin_config.x_rpc_device_fp}'
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://api-takumi-record.mihoyo.com/event/game_record_zzz/api/zzz/avatar/info?id_list[]={aid}&need_wiki=true&server=prod_gf_cn&role_id={uid}',cookies=cookies,headers=headers)
    json = r.json()
    return json

async def get_avatar_info_list(cookies,list,uid,user_id):
    id_list = {}
    for jso in list:
        key = ''.join(re.findall(r'[\u4e00-\u9fff0-9]+', str(jso['full_name_mi18n'])))
        value = str(jso['id'])
        id_list[key] = value
    info_list = []
    for key, value in id_list.items():
        json = await get_avater_info(cookies, value, uid)
        info_list.append(json)
    await save_list(info_list,user_id)


async def save_cookie(cookies,user_id):
    with open(f"{module_path}/ZZZ_data/cookies/{user_id}.json","w",encoding="utf-8") as f:
        json.dump(cookies,f,indent=4,ensure_ascii=False)

async def load_cookie(user_id):
    with open(f"{module_path}/ZZZ_data/cookies/{user_id}.json","r",encoding="utf-8") as f:
        cookies = json.load(f)
    return cookies

async def check_cookie(user_id):
    path = f"{module_path}/ZZZ_data/cookies/{user_id}.json"
    if os.path.exists(path):
        return True
    else:
        return False

async def save_avatar(avatar_id_list,user_id):
    with open(f"{module_path}/ZZZ_data/avatar/list/{user_id}.json","w",encoding="utf-8") as f:
        json.dump(avatar_id_list,f,indent=4,ensure_ascii=False)

async def save_list(info,user_id):
    with open(f"{module_path}/ZZZ_data/avatar/info/{user_id}.json","w",encoding="utf-8") as f:
        json.dump(info,f,indent=4,ensure_ascii=False)

async def check_avatar(user_id,name):
    with open(f"{module_path}/ZZZ_data/avatar/info/{user_id}.json","r",encoding="utf-8") as f:
        data = json.load(f)
    for i, item in enumerate(data):
        avatar = item['data']['avatar_list'][0]
        nm = avatar['name_mi18n']
        if fuzz.ratio(name, nm) > 85:
            return True, i
    return False, None