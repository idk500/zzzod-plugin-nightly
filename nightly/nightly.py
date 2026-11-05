"""Nightly 尝鲜版应用。

把代码源切到 idk500 增强源的 nightly 分支：写入代码源声明与用户选择后提示重启生效。
不进行任何游戏画面操作，运行即完成。

兼容旧版：早先绑定过 `zode` 分支的用户，配置里仍是旧分支名，这里一并改写为 nightly，
避免分支改名后更新失败。
"""

from typing import Any

import yaml
from one_dragon.base.operation.application_base import Application
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.utils import os_utils
from one_dragon.utils.log_utils import log
from zzz_od.context.zzz_context import ZContext

from . import nightly_const

# 增强源信息（CNB，大陆免代理直连）
NIGHTLY_REPOSITORY_ID = 'idk500_cnb'
NIGHTLY_REPOSITORY_LABEL = 'idk500 增强源 CNB（Nightly）'
NIGHTLY_REPOSITORY_URL = 'https://cnb.cool/zzz1d/ZODE.git'
NIGHTLY_BRANCH = 'nightly'
# 分支改名前的老名字，仅用于识别需要迁移的旧配置
LEGACY_BRANCH = 'zode'


class NightlyApp(Application):
    """Nightly 尝鲜版应用。"""

    def __init__(self, ctx: ZContext):
        Application.__init__(
            self,
            ctx=ctx,
            app_id=nightly_const.APP_ID,
            op_name=nightly_const.APP_NAME,
        )

    def handle_init(self) -> None:
        """初始化节点编排。"""
        Application.handle_init(self)

    @operation_node(name='切换到 Nightly 尝鲜版', is_start_node=True)
    def switch_to_nightly(self) -> OperationRoundResult:
        """写入增强源声明与用户选择，提示重启生效。"""
        current_url = self.ctx.env_config.repository_url
        current_branch = self.ctx.env_config.git_branch

        if current_url == NIGHTLY_REPOSITORY_URL and current_branch == NIGHTLY_BRANCH:
            return self.round_success(status='当前已是 Nightly 尝鲜版，无需重复切换')

        migrating = current_branch == LEGACY_BRANCH
        if not migrating and current_url != NIGHTLY_REPOSITORY_URL:
            log.info(f'代码源将从 {current_url} 切换到 {NIGHTLY_REPOSITORY_URL}')

        try:
            self._declare_repository()
        except Exception:  # noqa: BLE001 宽捕获写文件异常统一走失败提示
            log.error('写入代码源声明失败', exc_info=True)
            return self.round_fail(status='写入 config/repository.yml 失败，请查看日志')

        self.ctx.env_config.repository_url = NIGHTLY_REPOSITORY_URL
        self.ctx.env_config.git_branch = NIGHTLY_BRANCH

        if migrating:
            return self.round_success(
                status='已从旧的 zode 分支迁移到 nightly，请重启一条龙；重启后会自动更新，'
                       '若提示分支不存在，在「资源管理」重新选择代码源后同步一次',
            )
        return self.round_success(
            status='配置完成，请重启一条龙；重启后将自动从 nightly 分支更新代码'
                   '（重启前请勿手动同步代码）。想回官方版：资源管理里切回官方源 + main',
        )

    def _declare_repository(self) -> None:
        """把增强源与 nightly 分支写入 config/repository.yml。

        源声明已存在时不重复添加同一项；分支条目按最新文案覆盖，保证描述与当前定位一致。
        """
        repository_yml = os_utils.get_path_under_work_dir('config', 'repository.yml')
        with open(repository_yml, encoding='utf-8') as file:
            data: dict[str, Any] = yaml.safe_load(file) or {}

        repositories: dict[str, Any] = data.get('repositories') or {}
        options: dict[str, Any] = repositories.get('options') or {}
        branches: dict[str, Any] = repositories.get('branches') or {}

        options[NIGHTLY_REPOSITORY_ID] = {
            'label': NIGHTLY_REPOSITORY_LABEL,
            'url': NIGHTLY_REPOSITORY_URL,
            'use_proxy': False,
        }
        branches[NIGHTLY_BRANCH] = {
            'label': 'Nightly 尝鲜版',
            'desc': '激进跟进上游、尽力吸纳社区提交，可能不稳定；随时可在资源管理切回官方版',
        }

        repositories['options'] = options
        repositories['branches'] = branches
        data['repositories'] = repositories

        with open(repository_yml, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)
