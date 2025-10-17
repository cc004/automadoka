from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
import math

ONCE_STAMINA_COST = 10

@description('消耗体力石购买体力')
@name('购买体力')
@inttype('stamina_buy_count', '购买次数', 1, [i for i in range(1, 9)])
@texttype('stamina_retain_count', '保留体力石', '120')
@default(False)
class stamina_buy(Module):
    async def do_task(self, client: pcrclient):

        item_cnt = sum(
            item.num for item in client.data.resp.itemDataList
            if item.itemMstId == 202001
        )

        # 1) 检查体力石数量
        retain_cnt = int(self.get_config('stamina_retain_count'))
        if item_cnt <= retain_cnt:
            raise SkipError(f"体力石不足，当前体力石: {item_cnt}，保留体力石: {retain_cnt}")
        
        # 2) 计算需要购买的体力次数
        buy_count = self.get_config('stamina_buy_count')
        
        buy_count -= client.data.resp.userParamData.recoveryCount

        if buy_count <= 0:
            raise SkipError("体力购买次数已达上限")
        
        req = UserApiSetStaminaRecoverRequest()
        req.recoverType = 1 # 体力石购买
        req.itemMstId = 202001 # 体力石
        req.num = buy_count

        await client.request(req)

        self._log(f"购买了 {buy_count} 次体力，当前体力: {client.stamina()}")

@description('根据角色缺口扫荡最高等级素材本，如果材料溢出则扫荡经验本')
@name('智能体力扫荡')
@inttype('basic_stamina_5star', "5星角色魔力突破目标", 120, [i for i in range(1, 131)])
@inttype('basic_stamina_4star', "4星角色魔力突破目标", 110, [i for i in range(1, 131)])
@inttype('basic_stamina_3star', "3星角色魔力突破目标", 59, [i for i in range(1, 131)])
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

        to_repeat = client.stamina() // ONCE_STAMINA_COST

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

            def calcrate(target, given):
                def leakyrelu(x):
                    if x >=0: return x
                    else: return -math.log2(-x / given + 1) * given
                # 根据leakyrelu计算power变化量
                return (leakyrelu(target) - leakyrelu(target - given)) / given
            
            # 计算命中率
            rate = sum(
                calcrate(cost.get(i,0), cnt)
                for i, cnt in rewards.items()
            )

            if all(cost.get(i, 0) <= 0 for i in rewards):
                rate = -1
            
            mg_ = next(x for x in quest_group_mst if x.questGroupMstId == group_id)

            self._log(f"{mg_.name}效率：{rate: .0%}")
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

        client.data.resp.userParamData.stamina -= to_repeat * ONCE_STAMINA_COST
        
        self._log(f"扫荡了{to_repeat}次最高效率本：{mg.name} - {max_rate: .0%}")
