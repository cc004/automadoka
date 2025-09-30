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

@name('快速洗词条')
@default(False)
@inttype('filter_sub_selection_times', '重复次数', 1, [i for i in range(1, 1000)])
@texttype('filter_style_mst_id', '目标角色ID', '10010701')
@texttype('filter_style_selection_index', '目标技能石序列（1代表1号槽）', '1')
@texttype('filter_sub_selection_key', '目标词条ID列表', '4054,4034')
@booltype('filter_style_intersection_logic', '是否启用【或/OR】逻辑', False)
@description('洗洗洗洗洗洗洗洗洗')
class super_wash(Module):
    async def do_task(self, client: pcrclient):
        style_id = int(self.get_config('filter_style_mst_id'))
        selection_index = int(self.get_config('filter_style_selection_index'))
        repeat_times = self.get_config('filter_sub_selection_times')
        field_name = f"subSelectionAbilityMstIds{selection_index}"
        filter_keys_raw = self.get_config('filter_sub_selection_key')
        is_intersection_logic = self.get_config('filter_style_intersection_logic')
        if isinstance(filter_keys_raw, str):
            filter_keys = set(filter_keys_raw.split(','))
        elif isinstance(filter_keys_raw, list):
            filter_keys = set(str(i) for i in filter_keys_raw)
        else:
            filter_keys = set()

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

        for _ in range(repeat_times):
            try:
                req = SelectionAbilityApiLearnSubSelectionAbilityRequest()
                req.styleMstId = style_id
                req.selectionAbilityNum = selection_index
                req.lockIds = []
                req.permanentLockIds = []

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
