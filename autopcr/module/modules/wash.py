from typing import List, Set

from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import apiclient, ApiException
from ...db.database import db
from ...model.models import *
import random
import itertools
from collections import Counter

NONE = '未使用'

sub_selection_list: Dict[str, int] = {}
style_list: Dict[str, int] = {}

def get_sub_selection_list() -> List[str]:
    global sub_selection_list
    if not sub_selection_list and db.selection_ability_list:
        sub_selection_list = {NONE: 0}
        for item in db.selection_ability_list:
            if item.selectionAbilityType == 2:
                sub_selection_list[f'{item.selectionAbilityMstId}:{item.name}'] = item.selectionAbilityMstId
    return list(sub_selection_list.keys())

def get_style_list() -> List[str]:
    global style_list
    if not style_list and db.style_list and db.character_list and db.figure_list:
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
@inttype('filter_sub_selection_times', '重复次数', 1, [i for i in range(1, 1000)])
@singlechoice('filter_sub_selection_key_1', '目标词条1',  NONE, get_sub_selection_list)
@singlechoice('filter_sub_selection_key_2', '目标词条2',  NONE, get_sub_selection_list)
@singlechoice('filter_sub_selection_key_3', '目标词条3',  NONE, get_sub_selection_list)
@singlechoice('filter_style', '目标角色', '', get_style_list)

@texttype('filter_style_selection_index', '目标技能石序列（1代表1号槽）', '1')
@booltype('filter_style_intersection_logic', '是否启用【或/OR】逻辑', False)
@description('洗洗洗洗洗洗洗洗洗')
class super_wash(Module):
    async def do_task(self, client: pcrclient):

        style_name = self.get_config('filter_style')
        selection_index = int(self.get_config('filter_style_selection_index'))
        repeat_times = self.get_config('filter_sub_selection_times')
        field_name = f"subSelectionAbilityMstIds{selection_index}"
        is_intersection_logic = self.get_config('filter_style_intersection_logic')

        style_id = style_list[style_name]

        filter_keys = [
            sub_selection_list[self.get_config(f'filter_sub_selection_key_1')],
            sub_selection_list[self.get_config(f'filter_sub_selection_key_2')],
            sub_selection_list[self.get_config(f'filter_sub_selection_key_3')]
        ]

        if style_id == 0:
            raise AbortError("请先选择一个角色")
        
        filter_keys = set([str(x) for x in filter_keys if x != 0])

        try:
            req = SelectionAbilityApiGetSelectionAbilityDataListRequest()
            
            res = await client.request(req)
                            
        except:
            self._log(f"对象初始化失败: {str(e)} (code={e.result_code})")
            return

        selection_ability_data_list = res.selectionAbilityDataList
        selection_ability_data_dict = {item.styleMstId: item for item in selection_ability_data_list}
                    
        init_sub_ids_str = getattr(selection_ability_data_dict.get(style_id), field_name)
        init_current_sub_ids = set(init_sub_ids_str.split(',')) if init_sub_ids_str else set()
        if (filter_keys.intersection(init_current_sub_ids) if is_intersection_logic else filter_keys.issubset(init_current_sub_ids)):
            self._log("词条已符合，无需洗练")
            return

        samst = {
            x.selectionAbilityMstId : x.name
            for x in await db.mst(MstApiGetSelectionAbilityMstListRequest())
        }

        styleMst = {
            x.styleMstId : x.name
            for x in await db.mst(MstApiGetStyleMstListRequest())
        }

        style_name = styleMst.get(style_id, '未知风格')
        acquires = {}

        selection_ability_list = (await client.request(SelectionAbilityApiGetSelectionAbilityDataListRequest())).selectionAbilityDataList

        selection_ability_data = next(
            (x for x in selection_ability_list if x.styleMstId == style_id), None
        )

        if not selection_ability_data:
            raise AbortError(f"没有找到角色 {style_id} 的数据")
        
        lock_str = getattr(selection_ability_data, 'subSelectionLocks' + str(selection_index))

        if lock_str:
            permanent_lockIds_list = [int(x) for x in lock_str.split(',')]
            self._log(f"应用永久锁定词条: {permanent_lockIds_list}")
        else:
            permanent_lockIds_list = []


        for _ in range(repeat_times):
            try:
                req = SelectionAbilityApiLearnSubSelectionAbilityRequest()
                req.styleMstId = style_id
                req.selectionAbilityNum = selection_index
                req.lockIds = []
                req.permanentLockIds = permanent_lockIds_list

                res = await client.request(req)

            except ApiException as e:
                self._log(f"洗词条失败: {str(e)} (code={e.result_code})")
                break

            with open('sub_selection_temp.log', 'a') as fp:
                fp.write(res.json())
                fp.write('\n')

            selection_ability_data = res.selectionAbilityData
            sub_ids_str = getattr(selection_ability_data, field_name)
            current_sub_ids = set(sub_ids_str.split(',')) if sub_ids_str else set()
            
            ability_names = []
            for sub_id in current_sub_ids:
                try:
                    sid = int(sub_id)
                except Exception:
                    sid = None
                if sid is not None:
                    ability_names.append(samst.get(sid, f'未知词条({sub_id})'))
                else:
                    ability_names.append(f'未知词条({sub_id})')

            acquires.setdefault(style_name, []).extend(ability_names)

            if (filter_keys.intersection(current_sub_ids) if is_intersection_logic else filter_keys.issubset(current_sub_ids)):
                self._log("已洗到全部目标词条，STOP")
                break

        self._log(f"洗练完成，获得的词条：")

        for style, abilities in acquires.items():
            self._log(f"{style}:")
            ability_counts = Counter(abilities)
            for ability, count in ability_counts.items():
                ability_str = f"{ability} x{count}"
                self._log(f"  - {ability_str}")

