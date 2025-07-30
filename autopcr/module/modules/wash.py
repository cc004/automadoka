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
@texttype('filter_style_mst_id', '目标角色ID', '10800101')
@texttype('filter_style_selection_index', '目标角色技能石索引', '1')
@texttype('filter_sub_selection_key', '目标词条ID列表', '4054,4034')
@description('洗洗洗洗洗洗洗洗洗')
class super_wash(Module):
    async def do_task(self, client: pcrclient):
        style_id = int(self.get_config('filter_style_mst_id'))
        selection_index = int(self.get_config('filter_style_selection_index'))
        repeat_times = self.get_config('filter_sub_selection_times')

        filter_keys_raw = self.get_config('filter_sub_selection_key')
        if isinstance(filter_keys_raw, str):
            filter_keys = set(filter_keys_raw.split(','))
        elif isinstance(filter_keys_raw, list):
            filter_keys = set(str(i) for i in filter_keys_raw)
        else:
            filter_keys = set()

        samst = {
            x.selectionAbilityMstId : x.name
            for x in await db.mst(MstApiGetSelectionAbilityMstListRequest())
        }

        styleMst = {
            x.styleMstId : x.name
            for x in await db.mst(MstApiGetStyleMstListRequest())
        }

        acquires = {}

        for _ in range(repeat_times):
            try:
                req = SelectionAbilityApiLearnSubSelectionAbilityRequest()
                req.styleMstId = style_id
                req.selectionAbilityNum = selection_index
                req.lockIds = []

                res = await client.request(req)

            except ApiException as e:
                self._log(f"洗词条失败: {str(e)} (code={e.result_code})")
                break

            with open('sub_selection_temp.log', 'a') as fp:
                fp.write(res.json())
                fp.write('\n')

            selection_ability_data = res.selectionAbilityData
    
            field_name = f"subSelectionAbilityMstIds{selection_index}"
            sub_ids_str = getattr(selection_ability_data, field_name)
            current_sub_ids = set(sub_ids_str.split(',')) if sub_ids_str else set()
            
            style_name = styleMst.get(style_id, '未知风格')
            
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

            if filter_keys.issubset(current_sub_ids):
                self._log("洗到全部目标词条，ST0P")
                break

        self._log(f"洗练完成，获得的词条：")

        for style, abilities in acquires.items():
            self._log(f"{style}:")
            ability_counts = Counter(abilities)
            for ability, count in ability_counts.items():
                ability_str = f"{ability} x{count}"
                self._log(f"  - {ability_str}")
