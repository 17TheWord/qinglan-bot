import asyncio

from nonebot import logger, on_message
from nonebot.adapters.minecraft import BaseChatEvent
from nonebot_plugin_alconna import UniMessage

from ...service import target_service

on_mc_msg = on_message(priority=10)


@on_mc_msg.handle()
async def handle_mc_message(event: BaseChatEvent):
    server_name = event.server_name
    logger.debug(f"[MC消息] 来自服务器: {server_name}，消息内容: {event.message}")

    if not (target_list := target_service.get_targets(server_name)):
        logger.debug(f"[MC消息] 未找到服务器 {server_name} 的任何绑定目标，消息不广播")
        return

    tasks = []

    for target in target_list:
        logger.info(f"[MC消息] 正在向 {target.id}::{target.self_id} 广播消息")
        tasks.append(asyncio.create_task(send_message(target, str(event.message))))

    await asyncio.gather(*tasks)


async def send_message(target, message: str):
    try:
        await UniMessage(message).send(target=target)
    except Exception as e:
        logger.warning(f"[MC消息] 向 {target.id}::{target.self_id} 发送失败：{e}")
