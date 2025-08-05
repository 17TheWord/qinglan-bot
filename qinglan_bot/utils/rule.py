from nonebot.adapters.minecraft import Event as MCEvent
from nonebot.internal.adapter import Event


def rule_platform_message(event: Event) -> bool:
    """是否平台消息"""
    return not isinstance(event, MCEvent)
