"""用户设置（user option）的读写辅助。

对应接口 ``/api/user/save_option``（``UserApiSaveOptionRequest``）。
payload 一共 42 个字段，其中三个控制队伍详情是否公开：

==========================================  ========
``characterBuildDetailPublishSoloRaid``     总力战
``characterBuildDetailPublishMultiRaid``    团战
``characterBuildDetailPublishScoreAttack``  打分
==========================================  ========

**这个接口是整体替换，不是局部更新。** ``apiclient`` 序列化时用的是
``req.dict(by_alias=True)``，没有 ``exclude_none``（见
``autopcr/core/apiclient.py``），所以只提交三个字段会把其余设置全部写成 ``null``。

因此流程必须是：``UserApiLoadOptionRequest`` 读回当前配置 → 只翻转这三个开关 →
``UserApiSaveOptionRequest`` 整体写回。少任何一步都会把账号设置弄坏。

``sm`` 与 ``lastHomeAccessTime`` 是 ``RequestBase`` 上的字段，由 ``apiclient``
自动填充，不要手动传。

本模块只做纯数据处理，不依赖网络、模型包或模块框架，方便离线自测。
"""

from typing import Any, Dict, List, Tuple

# 开关字段
PUBLISH_SOLO_RAID = "characterBuildDetailPublishSoloRaid"
PUBLISH_MULTI_RAID = "characterBuildDetailPublishMultiRaid"
PUBLISH_SCORE_ATTACK = "characterBuildDetailPublishScoreAttack"

# 字段 -> 显示名
PUBLISH_LABELS = {
    PUBLISH_SOLO_RAID: "总力战",
    PUBLISH_MULTI_RAID: "团战",
    PUBLISH_SCORE_ATTACK: "打分",
}

# 需要提交的字段总数（40 个业务字段 + sm + lastHomeAccessTime），用于自检
SAVE_OPTION_FIELD_COUNT = 42


def build_option_payload(
    current: Dict[str, Any],
    *,
    hide_multi_raid: bool = True,
    hide_score_attack: bool = True,
) -> Tuple[Dict[str, Any], List[str]]:
    """把当前配置里的队伍展示开关关掉。

    返回 ``(新的配置, 本次真正被关闭的显示名列表)``。

    ``current`` 应当是 ``UserApiLoadOptionResponse.dict()`` 的结果——即从服务端
    读回的全量配置，而不是手工拼的几个字段。总力战始终关闭；团战、打分按参数决定。
    """
    data = dict(current)
    targets = [PUBLISH_SOLO_RAID]
    if hide_multi_raid:
        targets.append(PUBLISH_MULTI_RAID)
    if hide_score_attack:
        targets.append(PUBLISH_SCORE_ATTACK)

    changed: List[str] = []
    for key in targets:
        if data.get(key):
            changed.append(PUBLISH_LABELS[key])
        data[key] = False
    return data, changed
