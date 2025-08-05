from nonebot_plugin_alconna import Target


def get_formated_target(target: Target):
    return f"[{target.id}::{target.self_id}]"
