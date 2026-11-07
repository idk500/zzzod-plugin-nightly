from one_dragon_qt.services.app_setting.app_setting_provider import (
    AppSettingProvider,
    SettingType,
)

from . import nightly_const


class NightlyAppSetting(AppSettingProvider):
    """Nightly 切换器设置入口（防误触确认开关）。"""

    app_id = nightly_const.APP_ID
    setting_type = SettingType.FLYOUT

    @staticmethod
    def get_setting_cls() -> type:
        from .nightly_setting_flyout import NightlySettingFlyout

        return NightlySettingFlyout
