# 魔女召唤 / 魔女点赞（Link Raid）

「魔女召唤」对应 `autopcr/module/modules/raid.py` 里的 `self_raid` 模块，
走团战（Link Raid）的 `/api/multi_raid/*` 接口，用一段给定的伤害记录发一车
**仅自己可见**的团战房间。

同一个文件里的「魔女点赞」（`like_raid`）也一并修了 —— 它的 bug 在
`autopcr/model/handlers.py` 里，会让整个模块每次点赞都报错，见
「魔女点赞：为什么会『失效』」一节。

## 改动前后

改动前的行为有三处不顺手：

1. 自己还有没打完的团战时会**直接放弃** —— 日志打一句"已经有未结束的团战，无法发车"就返回，
   那一车永远停在半血
2. 战斗结果要**手填** `1:win / 2:lose / 3:timeout`，填错了结算记录就难看
3. 难度只能按「已通关 +1」，想回头补低难度做不到

改动后对齐了 RustMadoka 的做法：**先打完旧的、再补领奖励、最后发新车**，
结果自动判断，难度可选。

## 设置项

界面上的排列顺序（前端按 `config_order` 渲染）：

| 设置项 | 键 | 默认 | 说明 |
|---|---|---|---|
| Raid 氪体数 | `raid_recovery_count` | 0 | 体力不够时最多恢复几次 |
| 放入待秒列表 | `start_raid_queue` | 开 | 打完 boss 没死就丢进待秒列表 |
| 发车前自动领取已结束的奖励 | `start_raid_receive` | 开 | 把已结束未领奖的房间全部补领 |
| 有未结束的团战时先把它打完 | `start_raid_continue_open` | 开 | 关掉就退回旧的「直接放弃」 |
| 自动召唤次数 | `start_raid_times` | 1 | 1~6，一次运行处理几件事 |
| 目标难度 | `start_raid_difficulty` | 空 | 留空=自动打下一档；填 1~20 打指定档 |
| 自动判断战斗结果 | `start_raid_auto_result` | 开 | 关掉就用手填的那个值 |
| 手动战斗结果 | `start_raid_result` | 3 | 只在上面关掉时生效 |
| 队伍名/id | `start_raid_party` | 30 | 填数字当 ID，否则按队伍名找 |
| 伤害下限 / 上限 | `start_raid_damage_min/max` | 900000 / 1100000 | 每次发车在这个区间随机取一个 |

## 执行流程

一次运行按「自动召唤次数」循环，**每一轮只处理一件事**：

```text
读 top
  │
  ├─ 自己还有没结束的团战？
  │     ├─ 否 → 继续
  │     └─ 是 → continue_open 关着？→ 提示并结束
  │             └─ 开着 → 接手这个房间打完，本轮结束
  │
  ├─ 补领所有已结束但没领奖的**自己的**房间（receive）
  │     └─ 本次运行自己结算过的房间除外（打赢的结算可能已经发过奖励了）
  ├─ 今日发车次数到顶了？→ 结束
  ├─ 算难度（留空 = 已通关 +1，上限 20）
  ├─ 体力不够 → 用魔法戒指恢复（受 raid_recovery_count 限制）
  └─ 开房 → 发伤害 → 结算
```

「接手已有房间」和「开新房」共用同一段结算逻辑：都是
`get_multi_raid_info` 拿己方战斗单位 → 分块 `add_damage` → `finalize_stage_for_user`。

## 战斗结果判定

`start_raid_auto_result` 打开时（默认）：

```text
boss 剩余 HP > 0 且 本次伤害 >= 剩余 HP  →  1 (win)
否则                                    →  3 (timeout)
```

和 RustMadoka 的 `finish_open_raid` 是同一套规则。boss 已经没血（`hp <= 0`）不算 win ——
那种房间本来就该是已结束状态。

关掉自动判断时用手填的 `start_raid_result`；填了 1/2/3 之外的值会退回 timeout。

纯逻辑都在 `autopcr/util/raidoption.py`：

* `highest_unlocked_difficulty(cleared)` —— 已通关 +1，夹在 1~20
* `parse_raid_difficulty(raw, cleared)` —— 解析「目标难度」，返回 `(难度, 说明)`
* `resolve_battle_result(auto, manual, damage, hp)` —— 上面那张表
* `parse_raid_times(raw)` —— 召唤次数，夹在 1~6
* `pending_rewards(stages, rooms, my_id, skip=())` —— 挑出「已结束 + 属于自己 + 还没领奖」的房间

## 补领奖励必须按 userId 过滤

`multiRaidRoomDataList` **里含别人的房间** —— 同一场团战每个参战者各有一条记录。
RustMadoka 的真实抓包样本里，关卡 55 下同时存在 `userId: 20` 和 `userId: 10` 两条：

```json
"multiRaidRoomDataList":[
    {"multiRaidStageDataId":55,"questDataId":999,"userId":20,...},
    {"multiRaidStageDataId":55,"questDataId":77,"userId":10,...}]
```

`questDataId` 是绑在自己身上的，拿别人的去领必然被服务端拒掉，报
**「報酬の受け取りに失敗しました。」**，整轮召唤就此中断。

同一文件里上游自己的 `raid_support`（魔女救世）就按 `userId` 过滤过这个列表，
`_my_room()` 也过滤 —— 只有补领那几处漏了。现在统一走 `pending_rewards()`，
三处调用点（`self_raid._receive_pending`、基类 `receive_rewards`、`raid_reward`）共用：

```python
stage_map = {stage.multiRaidStageDataId: stage for stage in stages}
skipped = set(skip or ())
for room in rooms:
    if room.questDataId and room.questDataId in skipped:
        continue
    stage = stage_map.get(room.multiRaidStageDataId)   # 用 get，不能用 []（会 KeyError）
    if stage is None or not stage.isClosed:
        continue
    if room.userId != my_id or room.isReceivedReward or not room.questDataId:
        continue
```

顺带三点：

* 单个房间领不了不再把整轮带停 —— `_receive_pending` 捕获 `ApiException`，
  记一行「补领团战 X 失败：…，本次运行不再重试」继续，后面照常发车。
* 被拒的房间记进 `self._rejected_rewards`（`skip`），**本次运行内不再重复请求**。
  服务端在一次运行里不会改口，原来每轮都重试同一个房间，6 轮下来白跑 5 次请求
  并且刷 5 行同样的日志。
* 基类 `receive_rewards` 原来写的是 `stage_map[raid.multiRaidStageDataId]`，
  房间对应的关卡不在列表里就会 `KeyError`，换成 `.get()` 后一并修掉。

## 自己刚结算的房间不要再补领

按 `userId` 过滤之后，日志里仍然出现**自己**的房间被拒：

```
补领团战 156236858277 (关卡 220) 失败：報酬の受け取りに失敗しました。，跳过
```

这条报错是服务端返回的业务错误，不是网络问题：`/api/multi_raid/receive_reward`
回 HTTP 500、`status="Error"`，`errors[].reason` 就是这句日文 —— 服务端认为这个房间
**没有可领的报酬**。

原因：**打赢的 `finalize_stage_for_user` 可能已经把奖励发掉了**，之后 `get_top`
里那个房间却还挂着 `isReceivedReward=False`，再领一次就是重复领取。

证据（RustMadoka 自己的注释，`vnext/.../special_modes/group_public.rs:945-947`）：

> Python's reward module acts on a fresh get_top list, not on every quest ID
> remembered before finalize. **Winning finalize may already grant the reward**
> and remove that quest from the pending list.

它的对应做法是领奖前**重读一次 `get_top`**，然后：

* 房间不在 `top.rooms` 里 → 「本次战斗已不在待领奖列表，未重复领奖」
* `room.is_received_reward` → 「回读确认本次奖励已领取，未重复领奖」
* `!stage.is_closed` → 先不领

另一个佐证：上游 autopcr 和 RustMadoka **都只在一次运行的开始补领**，只领
**上一次运行**留下的房间 —— 从来不去领自己几秒前刚打完的房间。魔女召唤改成
6 轮循环后才会走到这条路径，所以这个报错是改完之后才第一次出现。

**改法**：`self_raid` 记下本次运行自己结算过的 `questDataId`（`_shipped_rooms`），
补领时把它们一起塞进 `skip`：

```python
skip=self._rejected_rewards | self._shipped_rooms
```

这些房间留到下一次运行（或「魔女舔盒」）再领，一次都不会丢。补领本身照旧在每轮
循环里跑，所以上一次运行留下的待领房间仍然会在第一轮就领掉。

失败日志也把定位字段全打出来（字段全部 `getattr` 兜底，协议换「代」删字段时
不会把真正的错误盖成 `ProtocolError`）：

```
补领团战 156236858277 (关卡 220) 失败：報酬の受け取りに失敗しました。 [Error/500]
（questDataId=…，isClosed=…，result=…，isReceivedReward=…，damage=…，endTime=…，
stageHp=…），本次运行不再重试
```

`receive_rewards`（基类）和 `raid_reward`（魔女舔盒）也改成逐房间容错：一个领不了
只记一行，不再让整个模块报错 —— 否则「魔女舔盒」是 `@default(True)`、跑在日常列表里，
一个卡住的房间会让每天的日常运行都带一个 ERROR。

## 魔女点赞：为什么会「失效」

`like_raid` 有三个问题，前两个对齐 RustMadoka 的 `run_link_like`
（`parent_ready.rs:200-270`），第三个是让「什么都没做」也能看见。

### 1. 崩在勋章配置上（真凶）

`autopcr/model/handlers.py` 里 `LikeApiExecLikeListResponse.update` 原来是这样取
「点赞一次给几个勋章」的：

```python
medal_once = next(
    x.num
    for x in mgr.config.friendConfig.friendMedal
    if x.dict(by_alias=True)['type'] == 'ExecLike'
)
```

**`next(...)` 没给默认值。** 只要 `friendConfig.friendMedal` 里没有 `type == 'ExecLike'`
那一行，就抛 `StopIteration`；而这是在 `async def update` 里，`StopIteration` 从协程
逃出来会被 CPython 转成 **`RuntimeError: coroutine raised StopIteration`**：

```text
抛出: RuntimeError -> coroutine raised StopIteration
```

`datamgr.request` 里是 `await resp.update(self, ...)`，就挂在请求链路中间 ——
所以**每成功点赞一次，整个「魔女点赞」模块立刻报错**，一条赞都记不上。

现在抽成 `raidoption.medal_per_like(medals)`：取不到返回 `0`，调用方据此跳过计数，
宁可少算一次也不能炸。测试里专门有一条 `test_missing_row_returns_zero_instead_of_raising`。

### 2. 不看服务端的 `isLiked`

`MultiRaidJoinUserInfo.isLiked` 是服务端标好的「这条赞我已经记过了」。上游没看它，
于是每次都把列表里的人重新点一遍，服务端回 `result=false`，既拿不到勋章，
**也不打任何日志** —— 看起来就是「点赞失效」。

RustMadoka 的做法是直接跳过：

```rust
if join.user_id == self_id || join.is_liked == Some(true) { continue; }
```

现在照抄，另外把 `userId == 0` / `multiRaidStageDataId == 0` 的无效行也过滤掉。

### 3. 勋章数用登录快照 + 全程静默

`todayFriendMedalCount` 其实是会被更新的 —— `handlers.py` 的
`LikeApiExecLikeListResponse.update` 每拿到一次勋章就累加（并夹到
`gainTodayFriendMedalMaxNum`）。但上游把它读在循环外面当成常量，于是
「好友勋章已满」这句永远不触发，日志里的 `(now/max_num)` 也一直是旧值。

现在改成读实时值，并在**一条赞都没点出去**时补一行汇总：

```text
没有可点赞的团战参与者
没有可点赞的团战参与者（2 条服务端已标记为已点赞）
```

否则「没有目标」和「模块挂了」在日志里长得一模一样。

## 发伤害为什么要分块

`MultiRaidApiAddDamageRequest` 单次能提交的伤害有上限（`raid/raidworker.py` 的
`DAMAGE_ONCE = 1000_0000`）。伤害超过上限就要拆成几包依次发，
`raidworker.send_damage()` 负责这件事。默认的 90w~110w 用不着拆，
但把伤害上限调大之后就会走到。

## 顺手修掉的两个隐患

改动前这段代码里有两处会出事：

1. `raid.hostUserId == client.data.resp.userData.userId` ——
   团战响应里只有 `userParamData`，`userData` 是**用户初始化响应**才有的字段，
   在团战上下文里读它纯属运气。现在统一走 `_my_open_stage()` / `_my_room()`，
   都读 `userParamData.userId`（和 `raid_support` 一致）。
2. `next(x for x in ... if ...)` 没给默认值 —— 当前没有开放的团战时 `next()` 会抛
   `StopIteration`，后面那句 `if not opening_raid` 是死代码。现在改成 `for` 循环里
   `return`，找不到就正常返回 `None`。

（同一个坑 `handlers.py` 里也有一处，而且更致命 —— 见「魔女点赞」一节。）

## 测试

```powershell
python -m unittest discover -s tests -p "test_raid_option.py" -v
```

`tests/test_raid_option.py` 只导入 `autopcr.util.raidoption` ——
模块本体在 `autopcr.module.modules` 包里，导入它会连带 `raid/raidrunner.py`，
而后者在模块顶层 `open('raid_config.json')`，这个文件在 `.gitignore` 里、
干净仓库上没有。

覆盖：难度自动/指定/越界夹取、结果自动判定（含刚好斩杀、boss 已死、非法手填值）、
召唤次数夹取、可领奖房间筛选（别人的房间、未结束、已领过、没房间号、关卡不在列表里、
`skip` 排除已试过的房间）、点赞勋章折算（`ExecLike` 行缺失/字段别名/数量为 0）。

流程本身（接手未结束的房间、补领、自动判断结果）需要一个带 `raid_config.json`
的工作区才能导入模块包，用假客户端单独验证过，没有进 `tests/`。

## 风险

* 战斗结果由本模块自己判断后上报，服务端是否复核尚未确认。
* `finalize_stage_for_user` 的 `battleLog` 由 `client.data.generate_battle_log()`
  按己方战斗单位现推，结构和上游 `start_clear()` 用的完全一致。
* 补领依赖 `isReceivedReward` 标记，标记没及时更新时会多领一次，那种情况由
  `_receive_pending` 的异常捕获兜住（记一行跳过，不再中断）。
* 打赢的 `finalize` 可能已经把奖励发掉，而 `get_top` 里那个房间仍是
  `isReceivedReward=False`。所以本次运行自己结算的房间一律不补领（见上一节），
  代价是这些房间要等下一次运行才领到。
* 「发车前自动领取」现在会领所有已结束的**自己的**房间，不限自己开的场；
  这是有意的 —— 参加了别人的团战同样有奖要领。
