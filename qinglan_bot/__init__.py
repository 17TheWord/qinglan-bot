from nonebot import get_driver, require

require("nonebot_plugin_orm")
require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")

from nonebot.plugin import PluginMetadata

from .config import Config
from .service import target_service

driver = get_driver()

driver.on_startup(target_service.load)


__plugin_meta__ = PluginMetadata(
    name="青岚Bot",
    description="基于NoneBot2与鹊桥的Minecraft Server消息互通机器人",
    homepage="https://github.com/17TheWord/qinglan_bot",
    usage="配置完成后在群聊发送消息即可同步至 Minecraft 服务器",
    config=Config,
    type="application",
)
from . import plugins as plugins
