import json

from nonebot import logger
from nonebot_plugin_alconna import Target
from nonebot_plugin_orm import get_session
from sqlalchemy import select

from ..database.model import TargetMapModel


class TargetService:
    def __init__(self):
        self.target_map: dict[str, set[Target]] = {}
        self.reverse_map: dict[Target, set[str]] = {}

    async def load(self):
        async with get_session() as session:
            result = await session.execute(select(TargetMapModel))
            for row in result.scalars().all():
                try:
                    target = Target.load(json.loads(row.target_data))
                    server_name = row.server_name
                    self._add_mapping_memory(server_name, target)
                except Exception as e:
                    logger.warning(f"载入目标失败: {e}")
            logger.info(
                f"TargetService: 成功载入 {sum(len(v) for v in self.target_map.values())} 个映射"
            )

    def _add_mapping_memory(self, server: str, target: Target):
        self.target_map.setdefault(server, set()).add(target)
        self.reverse_map.setdefault(target, set()).add(server)
        logger.debug(f"内存映射添加: {server} <-> {target}")

    def _remove_mapping_memory(self, server: str, target: Target):
        if server in self.target_map:
            self.target_map[server].discard(target)
            if not self.target_map[server]:
                del self.target_map[server]
        if target in self.reverse_map:
            self.reverse_map[target].discard(server)
            if not self.reverse_map[target]:
                del self.reverse_map[target]
        logger.debug(f"内存映射删除: {server} <-> {target}")

    async def add_mapping(self, server: str, target: Target):
        async with get_session() as session:
            model = TargetMapModel(
                server_name=server, target_data=json.dumps(target.dump())
            )
            session.add(model)
            await session.commit()
            self._add_mapping_memory(server, target)
            logger.info(f"数据库添加映射成功: {server} <-> {target}")

    async def remove_mapping(self, server: str, target: Target):
        async with get_session() as session:
            result = await session.execute(
                select(TargetMapModel).where(
                    TargetMapModel.server_name == server,
                    TargetMapModel.target_data == json.dumps(target.dump()),
                )
            )
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
                self._remove_mapping_memory(server, target)
                logger.info(f"数据库删除映射成功: {server} <-> {target}")
            else:
                logger.warning(f"尝试删除不存在的映射: {server} <-> {target}")

    def get_targets(self, server: str) -> set[Target]:
        return self.target_map.get(server, set())

    def get_servers(self, target: Target) -> set[str]:
        return self.reverse_map.get(target, set())

    def is_bound(self, server: str, target: Target) -> bool:
        return target in self.target_map.get(server, set())


target_service = TargetService()
