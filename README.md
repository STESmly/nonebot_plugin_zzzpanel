<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_zzzpanel

_✨ NoneBot 插件描述 ✨_

自己写的ZZZ角色数据获取插件
</div>

## 📖 介绍

能获取所有角色的练度（因为是用的官方api）


## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_zzzpanel

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_zzzpanel
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_zzzpanel"]

</details>

## 待完善的功能（更新较慢，所以期待pr哦）

- [ ] 所有米游的数据获取
- [ ] 单用户多个账号的登录与切换
- [ ] 圣遗物/遗器/驱动盘 评分系统相关（为了防止散套冲榜，我计划会加入针对每个角色定制一套套装评分权重，散套和毕业套的；评分差距约在40分左右）
- [ ] 优化面板样式
- [ ] playwright库自动下载依赖
- [ ] 加入管理员和群权限
- [ ] 加入功能菜单
- [ ] 完善查询角色面板时的名字（目前未设计角色别名库，只做了一定的模糊判断，例如api返回的是零号·安比，中间的符号不好打，输入零号安比即可）
- [ ] 想不到更多的了

## 指令大全

- ZZZ绑定
- ZZZ图鉴
- ZZZ练度+角色名字
- ZZZ更新数据\[无/图鉴/练度\]

## 配置

```bash
x_rpc_device_fp : 输入你常用设备的设备指纹
```

## 效果图展示

![demo](/example/效果图1.png)
![demo](/example/效果图2.png)
![demo](/example/效果图3.png)

