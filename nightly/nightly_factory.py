"""Nightly 尝鲜版工厂。

工厂文件必须以 _factory.py 结尾才能被自动发现。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application.application_factory import ApplicationFactory

from . import nightly_const
from .nightly_config import NightlyConfig

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class NightlyFactory(ApplicationFactory):
    """Nightly 尝鲜版工厂。"""

    def __init__(self, ctx: ZContext):
        ApplicationFactory.__init__(self, nightly_const)
        self.ctx: ZContext = ctx

    def create_application(self, instance_idx: int, group_id: str):
        from .nightly import NightlyApp

        return NightlyApp(self.ctx)

    def create_config(self, instance_idx: int, group_id: str):
        return NightlyConfig(instance_idx=instance_idx, group_id=group_id)
