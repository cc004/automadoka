from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *

ONCE_STAMINA_COST = 10

@description('根据角色缺口扫荡最高等级素材本，如果材料溢出则扫荡经验本')
@name('智能体力扫荡')
@inttype('basic_stamina_5star', "5星角色魔力突破目标", 120, [i for i in range(1, 121)])
@inttype('basic_stamina_4star', "4星角色魔力突破目标", 110, [i for i in range(1, 121)])
@inttype('basic_stamina_3star', "3星角色魔力突破目标", 59, [i for i in range(1, 121)])
@default(True)
class basic(Module):
    async def do_task(self, client: pcrclient):
        # 2) 获取训练任务数据
        train_quest = await client.request(QuestOutGameApiGetUserTrainingQuestDataListRequest())

        # 构造 cleared_group 映射
        cleared_group: Dict[int,int] = {
            r.questGroupMstId: r.clearedQuestStageMstId
            for r in train_quest.userQuestTrainingDataList
        }

        to_repeat = client.data.resp.userParamData.stamina // ONCE_STAMINA_COST

        if to_repeat <= 0:
            raise SkipError(f"体力不足最低耗体({ONCE_STAMINA_COST})")
        
        # 3) 拉取各类 Mst 列表并转为字典
        # styleMst
        style_mst = {
            m.styleMstId: m for m in
            await db.mst(MstApiGetStyleMstListRequest())
        }

        # paramUpMst
        param_up_mst: Dict[int, List[StyleStyleParamUpMstRecord]] = {}
        for p in await db.mst(MstApiGetStyleParamUpMstListRequest()):
            param_up_mst.setdefault(p.groupId, []).append(p)

        # paramUpCostMst
        param_up_cost_mst = {
            c.styleParamUpCostMstId: c for c in
            await db.mst(MstApiGetStyleParamUpCostMstListRequest())
        }

        # questGroupMst
        quest_group_mst = await db.mst(MstApiGetQuestGroupMstListRequest())

        # 4) 计算升级素材需求
        cost: Dict[int,int] = {}
        def add_cost(item_id: int, cnt: int):
            if item_id and cnt:
                cost[item_id] = cost.get(item_id, 0) + cnt

        for style in client.data.resp.styleDataList:
            mst = style_mst[style.styleMstId]
            if mst.rarity == 5:
                targetPriority = self.get_config('basic_stamina_5star')
            elif mst.rarity == 4:
                targetPriority = self.get_config('basic_stamina_4star')
            elif mst.rarity == 3:
                targetPriority = self.get_config('basic_stamina_3star')
            else:
                self._log(f"未识别的角色星级: {mst.rarity}")
                continue
                
            for line in param_up_mst[mst.paramUpGroupId]:
                if style.lastParamUpPriority >= line.priority:
                    continue
                if line.priority > targetPriority:
                    continue
                c = param_up_cost_mst[line.styleParamUpCostMstId]
                add_cost(c.useItemMstId1, c.useItemNum1)
                add_cost(c.useItemMstId2, c.useItemNum2)
                add_cost(c.useItemMstId3, c.useItemNum3)
                add_cost(c.useItemMstId4, c.useItemNum4)
                add_cost(c.useItemMstId5, c.useItemNum5)
                add_cost(c.useItemMstId6, c.useItemNum6)

        # 扣除已有物品数量
        for item in client.data.resp.itemDataList:
            if item.itemMstId in cost:
                cost[item.itemMstId] -= item.num
            else:
                cost[item.itemMstId] = -item.num

        # 5) 拉取 QuestStageMst & QuestRewardMst
        quest_mst = await db.mst(MstApiGetQuestStageMstListRequest())
        quest_reward = await db.mst(MstApiGetQuestRewardMstListRequest())

        # 6) 选取最优组队来刷体力
        max_group = 101
        max_rate = 0.0
        
        if all(x <= 0 for x in cost.values()):
            # 物品充足，直接返回
            self._log(f"物品充足，仅刷取经验")
        else:
            for group_id, stage_id in cleared_group.items():
                # 找到关卡记录
                qr = next(q for q in quest_mst if q.questStageMstId == stage_id)
                # 收集奖励
                rewards: Dict[int,int] = {}
                def add_reward(iid,cnt):
                    if iid and cnt:
                        rewards[iid] = rewards.get(iid,0) + cnt

                for rw in [r for r in quest_reward if r.rewardGroupId == qr.rewardGroupId]:
                    add_reward(rw.objectId, rw.num)

                def calcrate(given, target):
                    def leakyrelu(x):
                        if x >=0: return x
                        else: return 0.01 * x
                    # 根据leakyrelu计算power变化量
                    return (leakyrelu(target) - leakyrelu(target - given)) / target
                
                # 计算命中率
                rate = sum(
                    calcrate(cost.get(i,0), cnt)
                    for i, cnt in rewards.items()
                )
                if rate > max_rate:
                    max_rate = rate
                    max_group = group_id

        # 输出
        mg = next(q for q in quest_group_mst if q.questGroupMstId == max_group)

        # sweep
        if to_repeat <= 0: return
        
        req_skip = QuestBattleApiSkipQuestBattleRequest()
        req_skip.questStageMstId = cleared_group[max_group]
        req_skip.isArchiveEvent = False
        req_skip.repeatNum = to_repeat
        await client.request(req_skip)
        
        self._log(f"扫荡了{to_repeat}次最高效率本：{mg.name} - {max_rate: .0%}")
