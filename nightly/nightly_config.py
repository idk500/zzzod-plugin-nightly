from one_dragon.base.operation.application.application_config import ApplicationConfig

from . import nightly_const


class NightlyConfig(ApplicationConfig):
    """Nightly 尝鲜版配置。"""

    def __init__(self, instance_idx: int, group_id: str):
        ApplicationConfig.__init__(
            self,
            app_id=nightly_const.APP_ID,
            instance_idx=instance_idx,
            group_id=group_id,
        )

    @property
    def confirm_switch(self) -> bool:
        """确认切换：防误触闸，未勾选时运行只会提示去设置。"""
        return self.get('confirm_switch', False)

    @confirm_switch.setter
    def confirm_switch(self, new_value: bool) -> None:
        self.update('confirm_switch', new_value)
