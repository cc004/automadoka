from typing import List, Optional

from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient, ApiException
from ...db.database import db
from ...model.models import *
from collections import Counter

sub_selection_list = {}
style_list = {}

EFFECT_ID_RULES = (
    (31, ('最大HP', '最大ＨＰ', '最大生命')),
    (32, ('攻撃力', '攻击力')),
    (33, ('防御力', '防御力')),
    (34, ('スピード', '速度')),
    (35, ('クリティカル率', '暴击率')),
    (36, ('クリティカルダメージ', '暴击伤害', '暴击傷害')),
    (37, ('ブレイク特効', 'Break特效', '破防特效')),
    (38, ('HP回復量', 'HP恢复量', 'HP回復量')),
    (39, ('デバフ命中率', '减益命中率', 'Debuff命中率')),
    (40, ('デバフ耐性', '减益抗性', 'Debuff耐性')),
)

# 游戏内筛选的词条稀有度分组（conditions.subRarityGroups）
SUB_RARITY_GROUP_CANDIDATES = [1, 2, 3]

def get_effect_id(name: str) -> Optional[int]:
    for effect_id, keywords in EFFECT_ID_RULES:
        if any(k in name for k in keywords):
            return effect_id
    return None

def get_sub_selection_list() -> List[str]:
    if not db.selection_ability_list: return []
    
    global sub_selection_list
    sub_selection_list = {}
    for item in db.selection_ability_list:
        if item.selectionAbilityType == 2:
            sub_selection_list[f'{item.selectionAbilityMstId}:{item.name}'] = item.selectionAbilityMstId
    return list(sub_selection_list.keys())

def get_style_list() -> List[str]:
    if not db.character_list or not db.figure_list: return []
    
    global style_list
    style_list = {'': 0}
    char_dict = {x.characterMstId: x.name for x in db.character_list}
    figure_dict = {
        x.styleFigureMstId: char_dict.get(x.characterMstId, f'未知角色({x.characterMstId})')
        for x in db.figure_list
    }
    for item in db.style_list:
        name = figure_dict.get(item.styleFigureMstId, f'未知角色({item.styleFigureMstId})')
        style_list[f'{item.styleMstId}:[{item.name}]{name}'] = item.styleMstId

    return list(style_list.keys())

@name('快速洗词条')
@default(False)
@inttype('filter_sub_selection_times', '工具重复次数', 1, [i for i in range(1, 1000)])
@inttype('filter_sub_selection_times_per_time', '每次重复次数（游戏内）', 20, [i for i in range(1, 1000)])
@booltype('filter_style_intersection_logic', '是否启用【或/OR】逻辑', False)
@multichoice('filter_sub_rarity_groups', '游戏内筛选稀有度组', [3], SUB_RARITY_GROUP_CANDIDATES)
@multisearch('filter_sub_selection_keys', '目标词条', [], get_sub_selection_list)
@texttype('filter_style_selection_index', '目标技能石序列（1代表1号槽）', '1')
@singlechoice('filter_style', '目标角色', '', get_style_list)
@description('洗洗洗洗洗洗洗洗洗')
class super_wash(Module):
    async def do_task(self, client: pcrclient):

        style_name = self.get_config('filter_style')
        selection_index = int(self.get_config('filter_style_selection_index'))
        repeat_times = self.get_config('filter_sub_selection_times')
        repeat_times_per_time = self.get_config('filter_sub_selection_times_per_time')
        field_name = f"subSelectionAbilityMstIds{selection_index}"
        is_intersection_logic = self.get_config('filter_style_intersection_logic')
        sub_rarity_groups = sorted(self.get_config('filter_sub_rarity_groups'))
        if not sub_rarity_groups:
            raise AbortError("请至少选择一个游戏内筛选稀有度组")

        style_id = style_list.get(style_name, 0)
        if style_id == 0:
            raise AbortError("请先选择一个角色")

        filter_ids = [
            sub_selection_list[key]
            for key in self.get_config('filter_sub_selection_keys')
            if key in sub_selection_list
        ]
        if not filter_ids:
            raise AbortError("请至少选择一个目标词条")
        filter_keys = set(str(x) for x in filter_ids)

        samst = {
            x.selectionAbilityMstId : x.name
            for x in await db.mst(MstApiGetSelectionAbilityMstListRequest())
        }

        effect_ids = set()
        for sid in filter_ids:
            ability_name = samst.get(sid, '')
            effect_id = get_effect_id(ability_name)
            if effect_id is None:
                self._warn(f"无法识别词条 {sid}:{ability_name} 的类型，不加入游戏内筛选条件")
            else:
                effect_ids.add(effect_id)
        if not effect_ids:
            raise AbortError("所选目标词条均无法识别类型，无法设置游戏内筛选条件")
        effect_ids = sorted(effect_ids)

        self._log(f"目标词条: {', '.join(samst.get(sid, str(sid)) for sid in filter_ids)}")
        self._log(f"游戏内筛选 subRarityGroups: {sub_rarity_groups}, effectIds: {effect_ids}，逻辑: {'或/OR' if is_intersection_logic else '且/AND'}")

        def is_satisfied(sub_ids: set) -> bool:
            return bool(filter_keys.intersection(sub_ids)) if is_intersection_logic else filter_keys.issubset(sub_ids)

        try:
            res = await client.request(SelectionAbilityApiGetSelectionAbilityDataListRequest())
        except ApiException as e:
            self._log(f"对象初始化失败: {str(e)} (code={e.result_code})")
            return

        selection_ability_data = next(
            (x for x in res.selectionAbilityDataList if x.styleMstId == style_id), None
        )
        if not selection_ability_data:
            raise AbortError(f"没有找到角色 {style_id} 的数据")

        init_sub_ids_str = getattr(selection_ability_data, field_name)
        init_current_sub_ids = set(init_sub_ids_str.split(',')) if init_sub_ids_str else set()
        if is_satisfied(init_current_sub_ids):
            self._log("词条已符合，无需洗练")
            return

        styleMst = {
            x.styleMstId : x.name
            for x in await db.mst(MstApiGetStyleMstListRequest())
        }
        style_name = styleMst.get(style_id, '未知风格')
        acquires = {}
        total_attempts = 0

        lock_str = getattr(selection_ability_data, 'subSelectionLocks' + str(selection_index))
        mst_id = getattr(selection_ability_data, 'mainSelectionAbilityMstId' + str(selection_index))

        if lock_str:
            permanent_lockIds_list = [int(x) for x in lock_str.split(',')]
            self._log(f"应用永久锁定词条: {permanent_lockIds_list}")
        else:
            permanent_lockIds_list = []

        for _ in range(repeat_times):
            try:
                req = SelectionAbilityApiLearnSubSelectionAbilityRepeatRequest()
                req.styleMstId = style_id
                req.selectionAbilityMstId = mst_id
                req.lockIds = []
                req.permanentLockIds = permanent_lockIds_list
                req.maxAttemptCount = repeat_times_per_time
                req.conditions = SelectionAbilityApiLearnSubSelectionAbilityRepeatConditions(
                    subRarityGroups=sub_rarity_groups,
                    effectIds=effect_ids,
                )

                res = await client.request(req)

            except ApiException as e:
                self._log(f"洗词条失败: {str(e)} (code={e.result_code})")
                break

            selection_ability_data = res.selectionAbilityData
            sub_ids_str = getattr(selection_ability_data, field_name)
            current_sub_ids = set(sub_ids_str.split(',')) if sub_ids_str else set()

            drawn_ids = [
                slot.subSelectionAbilityMstId
                for attempt in (res.attemptHistory or [])
                for slot in (attempt.drawnSlots or [])
            ] or [int(x) for x in current_sub_ids if x.isdigit()]
            total_attempts += res.attemptCount or 0
            acquires.setdefault(style_name, []).extend(
                samst.get(sid, f'未知词条({sid})') for sid in drawn_ids
            )
            self._log(f"本轮尝试 {res.attemptCount} 次，游戏内条件{'已' if res.isConditionMet else '未'}满足，当前词条: "
                      + ', '.join(samst.get(int(x), f'未知词条({x})') for x in sorted(current_sub_ids) if x.isdigit()))

            if is_satisfied(current_sub_ids):
                self._log("已洗到全部目标词条，STOP")
                break

        self._log(f"洗练完成，共尝试 {total_attempts} 次，抽到的词条：")

        for style, abilities in acquires.items():
            self._log(f"{style}:")
            ability_counts = Counter(abilities)
            for ability, count in ability_counts.most_common():
                ability_str = f"{ability} x{count}"
                self._log(f"  - {ability_str}")
