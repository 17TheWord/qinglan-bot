import asyncio

from nonebot import get_bot, logger, on_message
from nonebot_plugin_alconna.uniseg import MsgTarget, UniMsg

from ...service import target_service
from ...utils import get_formated_target, rule_platform_message

platform_msg = on_message(rule=rule_platform_message)


@platform_msg.handle()
async def _(msg: UniMsg, target: MsgTarget):
    if not (server_names := target_service.get_servers(target)):
        logger.debug(
            f"[平台消息] 当前目标 {get_formated_target(target)} 未绑定任何 MC 服务器，消息不转发"
        )
        return

    msg_text = msg.extract_plain_text()
    logger.info(
        f"[平台消息] 来自 {get_formated_target(target)}，准备同步到 MC 服务器：{server_names}"
    )

    tasks = [
        asyncio.create_task(send_to_mc(server_name, msg_text))
        for server_name in server_names
    ]
    await asyncio.gather(*tasks)


async def send_to_mc(server_name: str, msg_text: str):
    try:
        bot = get_bot(server_name)
    except Exception:
        logger.warning(f"[平台消息] 无法获取 MC 机器人实例，服务器名: {server_name}")
        return

    try:
        logger.info(f"[平台消息] 发送消息到 {server_name} 服务器")
        await bot.send_msg(message=msg_text)
    except Exception as e:
        logger.warning(f"[平台消息] 发送至 {server_name} 服务器失败: {e}")
