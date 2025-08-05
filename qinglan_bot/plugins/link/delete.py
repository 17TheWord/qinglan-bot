from nonebot import on_command
from nonebot.internal.adapter import Message
from nonebot.params import CommandArg
from nonebot_plugin_alconna import MsgTarget

from ...service import target_service
from ...utils.rule import rule_platform_message

unlink_cmd = on_command("unlink", rule=rule_platform_message)


@unlink_cmd.handle()
async def _(target: MsgTarget, args: Message = CommandArg()):
    server_name = args.extract_plain_text().strip()
    if not server_name:
        await unlink_cmd.finish("请输入服务器名称！")

    if not target_service.is_bound(server_name, target):
        await unlink_cmd.finish(f"该聊天未绑定服务器 {server_name}")

    await target_service.remove_mapping(server_name, target)
    await unlink_cmd.finish(f"成功解绑服务器 {server_name}")
