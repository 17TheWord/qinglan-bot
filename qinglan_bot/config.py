from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    """配置"""


plugin_config = get_plugin_config(Config)
