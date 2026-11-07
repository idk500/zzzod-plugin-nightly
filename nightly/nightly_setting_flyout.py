from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout

from one_dragon_qt.utils.config_utils import get_prop_adapter
from one_dragon_qt.widgets.app_setting.app_setting_flyout import AppSettingFlyout
from one_dragon_qt.widgets.setting_card.switch_setting_card import SwitchSettingCard

from . import nightly_const


class NightlySettingFlyout(AppSettingFlyout):
    """Nightly 切换器配置弹出框：防误触确认开关。"""

    def _setup_ui(self, layout: QVBoxLayout) -> None:
        self.confirm_switch_opt = SwitchSettingCard(
            icon='',
            title='确认切换到 Nightly 尝鲜版',
            content='防误触保护：勾选后运行本应用才会真正改写代码源配置；'
                    '想切回官方版，在「资源管理」选官方源 + main 同步一次',
            margins=self.card_margins,
        )
        layout.addWidget(self.confirm_switch_opt)

    def init_config(self) -> None:
        config = self.ctx.run_context.get_config(
            app_id=nightly_const.APP_ID,
            instance_idx=self.ctx.current_instance_idx,
            group_id=self.group_id,
        )
        self.confirm_switch_opt.init_with_adapter(
            get_prop_adapter(config, 'confirm_switch')
        )
