from nonebot import on_command
from nonebot.internal.adapter import Message
from nonebot.params import CommandArg
from nonebot_plugin_alconna import MsgTarget

from ...service import target_service
from ...utils.rule import rule_platform_message

link_cmd = on_command("link", rule=rule_platform_message)


@link_cmd.handle()
async def handle_link(target: MsgTarget, args: Message = CommandArg()):
    if not (server_name := args.extract_plain_text()):
        await link_cmd.finish("请输入服务器名称！")

    if target_service.is_bound(server_name, target):
        await link_cmd.finish(f"该聊天已绑定服务器 {server_name}")

    await target_service.add_mapping(server_name, target)
    await link_cmd.finish(f"成功绑定服务器 {server_name}")
