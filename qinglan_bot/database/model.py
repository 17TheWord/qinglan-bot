import time

from nonebot_plugin_orm import Model as BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Model(BaseModel):
    """模型基类"""

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[int] = mapped_column(default=int(time.time() * 1000))
    updated_at: Mapped[int] = mapped_column(default=int(time.time() * 1000))


class TargetMapModel(Model):
    """聊天同步目标模型"""

    __tablename__ = "tb_target_map"

    server_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_data: Mapped[str] = mapped_column(String(255), nullable=False)
