# 总力战（Solo Raid）

总力战是游戏里的月度 boss 挑战活动，接口前缀 `/api/solo_raid/`。本文说明
本仓库中「总力战」功能的实现：数据从哪来、一次战斗怎么走完、战斗日志是怎么生成的，
以及不同结算方式的风险边界。

功能挂在 Web 界面的**危险**页，默认关闭。

## 结论先说

总力战的伤害数值**由客户端上报**。`finalize_stage_for_user` 接收一份完整的战斗回放，
服务端只负责按上报结果结算分数与奖励。这与团战的 `MultiRaidApiAddDamageRequest`
是同一个思路。

因此实现分成两条路：

| 结算方式 | 走哪个接口 | 能否打未通关难度 | 风险 |
|---|---|---|---|
| 模拟完整日志 / 极简日志 | 自己生成 battleLog 提交 | 可以 | 依赖服务端不校验日志真实性 |
| 服务端跳过战斗 | 官方 `skip_quest_battle` | 不可以，要求该难度已通关 | 最低，是游戏自带机制 |

前两条路的战斗日志由本仓库自行"推理"生成；第三条完全不用日志，由服务端自己模拟。

## 文件构成

| 文件 | 职责 |
|---|---|
| `autopcr/module/modules/solo_raid_battle.py` | 模块本体：读取配置、串联流程、输出日志 |
| `raid/soloraidworker.py` | 主数据读取、战斗单位构造、战力门槛、战斗执行 |
| `autopcr/util/soloraid_battlelog.py` | 战斗日志生成器，纯数据、不依赖网络 |
| `autopcr/module/modules/hide_party.py` | 配套模块：关闭队伍展示（见下） |
| `tests/test_soloraid_battlelog.py` | 生成器的离线测试 |
| `tests/test_hide_party.py` | 隐藏队伍与战力门槛的离线测试 |
| `autopcr/module/modules/__init__.py` | 挂载到 `danger_modules` |

`autopcr/util/soloraid_battlelog.py` 不导入任何模型或网络代码，输入是普通对象、
输出是可直接提交的 JSON，所以能完全离线自测。

## 设置项

| 配置键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `solo_raid_difficulty` | 单选 | `4`（very hard） | easy / normal / hard / very hard / extra / crisis；有战力门槛的难度会把要求标在名字后面 |
| `solo_raid_kill_timing` | 单选 | `instant` | 秒杀 / 中间时间点 / 最后关头 |
| `solo_raid_party` | 文本 | `1` | 队伍名或队伍 ID |
| `solo_raid_battle_log_mode` | 单选 | `simulate` | 模拟完整日志 / 极简日志 / 服务端跳过战斗 |
| `solo_raid_times` | 整数 | `1` | 执行次数，1~5 |
| `solo_raid_show_all_boss` | 开关 | 关 | 显示当前赛季全部难度的 boss 数据 |

界面上这些项的排列顺序是：难度 → 斩杀时机 → 出战队伍名/id → 结算方式 → 执行次数 →
显示全部难度的 boss 数据。

顺序由装饰器的书写位置决定，容易搞反：前端按 `config_order` 渲染，而 `config_order`
等于装饰器**自下而上**的顺序，所以想让某一项排在最前面，它的装饰器要写在最下面。
模块里对此有注释，改动时不要按直觉调。

选择型候选项统一用 `"值:显示名"` 的字符串格式，取值时按第一个冒号切开。
所以显示名里可以随便加括号标注，不影响取值。

## 战力门槛

战力明显不达标却能结算出击杀，结算记录上一眼就能看出来。所以高难度设了队伍战力下限：

| 难度 | 名称 | 要求队伍战力 |
|---|---|---|
| 4 | very hard | 60000（6 万） |
| 5 | extra | 70000（7 万） |
| 6 | crisis | 80000（8 万） |

easy / normal / hard 不设门槛。

要求会标在难度选项的名字后面（如 `very hard（需战力 6万）`），选的时候就能看到。
执行时再校验一次：读取所选队伍的 `partyPower`，不达标直接中断，提示

```text
xdx，战力不够容易被别人看出开挂，请到达战力标准再使用
```

具体差多少会写在日志里。门槛值集中在 `raid/soloraidworker.py` 的 `MIN_PARTY_POWER`，
判断逻辑是纯函数 `check_party_power(difficulty, power)`，改阈值只改这一处。

显示走 `format_power()`：10000 的整数倍显示成「N万」，否则退回千分位精确数字
（避免出现 `6.0万` 这种四舍五入过的门槛）。

队伍战力取自 `client.data.resp.partyDataList` 里对应 `partyDataId` 的 `partyPower`，
读不到按 0 处理。

## 数据链

boss 数据全部来自服务端主数据，赛季每月月初更换 boss 后会自动跟着变，不需要改代码。

```text
MstApiGetSoloRaidMstListRequest          赛季列表（startTime / battleEndTime / endTime）
  → 取 startTime <= 现在 <= battleEndTime 的那一个
MstApiGetSoloRaidStageMstListRequest     该赛季各难度的关卡
  → 按 difficulty 过滤
MstApiGetQuestEnemyAppearanceMstListRequest
                                         按 questStageMstId 取 boss 部位
  → 血量、攻防、速度、弱点元素、wave、是否主目标
MstApiGetQuestEnemySkillSetMstListRequest
                                         按 enemySkillSetId 取敌人技能
```

难度与关卡 ID 的对应关系是：

```text
soloRaidStageMstId = 赛季ID * 100 + 难度
```

难度取 1~6，依次是 easy、normal、hard、very hard、extra、crisis。

主数据通过 `db.mst(...)` 读取，需要客户端已经登录并完成 `db.update(client)`。
模块由框架在登录后调用，这一点天然满足。

## 战斗流程

### 模拟日志 / 极简日志

```text
SoloRaidApiInitializeStageRequest        进本，拿到 questDataId
  → SoloRaidApiGetSoloRaidInfoRequest    取我方出战单位（allyBattleUnitList）
  → build_solo_raid_battle_log(...)      推理出 battleLog 与 battleInfo
  → SoloRaidApiFinalizeStageForUserRequest
                                         提交 questDataId / result / battleInfo /
                                         battleLog / autoMode，结算
```

进本与结算之间各有 1 秒间隔，避免请求过密。

`InitializeStageRequest` 固定使用 `challengeType=Normal`、`soloRaidStageDataId=0`、
`styleRentalUsingStatus=NotUsing`。

### 服务端跳过战斗

```text
SoloRaidApiInitializeStageRequest        进本，拿到 questDataId
  → SoloRaidApiSkipQuestBattleRequest(repeatNum=N)
                                         服务端模拟战斗并结算，不需要 battleLog
```

这是游戏自带的官方机制。仓库里原有的「扫荡总力战」（`sweep.py`）用的就是它，
区别是那边不调 `initialize_stage`、只做一次批量跳过；本模块走完整的
"进本 → 跳过"，因此能指定难度。

前提是该难度**已经通关过一次**，否则服务端会拒绝。想用这条低风险路径打新难度，
需要先手动通关一次。

## 战斗日志结构

提交的 `battleLog` 是一个 JSON 字符串：

```json
{"Commands": [...], "ResultBattleUnits": [...], "ResultRound": 3}
```

`Commands` 是逐条战斗指令，共三种：

| 指令 | 作用 |
|---|---|
| `CommandBeginTurn` | 回合/行动开始，携带 `TurnActOrderUnitInfo`（行动顺序） |
| `CommandExecuteCommonAct` | 单位普通行动、异常状态结算 |
| `CommandSkill` | 技能释放，伤害就在 `AffectedUnitNoticeList[].Damages[].DamageValue` |

指令类型字符串与服务端序列化格式一致：

```text
ReDriveBattleCore.Command.CommandBeginTurn, Assembly-CSharp
ReDriveBattleCore.Command.CommandExecuteCommonAct, Assembly-CSharp
ReDriveBattleCore.Command.CommandSkill, Assembly-CSharp
```

`ResultBattleUnits` 是终局单位状态。**阵亡的敌方单位不带 `HP` 字段**，这一点与抓包一致，
生成器里有对应的分支处理。

`battleInfo` 表示"敌人已全灭"的终局状态，共 9 个键：

```text
wave, enemyInfoList, enemyLinkHp, enemyCountDownNum, enemyCountDownDamage,
isSeasonBuffActive, seasonBuffPoint, seasonBuffTurnGaugeValue, nextEnemyIndex
```

### 行动顺序与时间

生成器按速度模拟行动顺序，几个常量取自抓包：

| 常量 | 值 | 含义 |
|---|---|---|
| `ROUND_TIME` | 115.0 | 一个回合对应的行动时间 |
| `ACTION_GAUGE` | 1000.0 | 行动槽填满所需距离，速度越快间隔越短 |
| `GAUGE_SCALE` | 0.1 | 日志里 `GaugeValue` 的量纲缩放 |

每回合所有存活单位按"我方优先、速度从高到低"排一次序，逐个产生
`BeginTurn` + `CommonAct` + `Skill` 三条指令。

### 斩杀时机与伤害分摊

斩杀时机决定 `ResultRound` 落在第几回合：

| 时机 | 目标回合 | 斩杀发生在该回合的第几个我方行动 |
|---|---|---|
| `instant` 秒杀 | 1 | 第 1 个 |
| `middle` 中间 | `ceil(limit_round / 2)` | 中间那个 |
| `last` 最后关头 | `limit_round` | 最后一个 |

伤害分摊的规则是：总伤害取 `boss_max_hp * 1.02`，前面的命中合计分摊 35%
（越靠后权重越高），**最后一击独占剩余 65%** 并负责斩杀，标记 `IsDead`。
其余部位在最后一击一并判死。

这样做的目的是让日志看起来像一场正常的战斗，而不是"一刀秒满血 boss"。

### 单位 ID 约定

我方单位用 `battleUnitDataId`（正数），敌方单位按出场顺序分配为 `-1, -2, ...`。
只把**最终波次**的敌人转成战斗单位，`wave` 取主数据里的最大值。

### 极简模式

`minimal` 模式把 `Commands` 置空，只提交 `ResultBattleUnits`（全部敌人标记阵亡）
和 `ResultRound`。它比模拟模式更短，但也更"不像"一场真实战斗。

## 协议兼容自检

游戏大版本更新时，autopcr 会整体重新生成协议模型（见
[协议模型自动更新](protocol-model-updates.md)），`from autopcr.model.models import *`
拿到的是惰性代理。若某个类在新协议里被改名或移除，调用时才会抛 `ProtocolError`，
堆栈很难看懂。

模块在 `do_task` 开头做一次自检，`_REQUIRED_PROTOCOL` 列出了全部依赖项：

```text
requests: SoloRaidApiInitializeStageRequest / SoloRaidApiGetSoloRaidInfoRequest /
          SoloRaidApiFinalizeStageForUserRequest / SoloRaidApiGetTopRequest /
          SoloRaidApiSkipQuestBattleRequest
requests: MstApiGetSoloRaidMstListRequest / MstApiGetSoloRaidStageMstListRequest /
          MstApiGetQuestEnemyAppearanceMstListRequest /
          MstApiGetQuestEnemySkillSetMstListRequest
common:   SoloRaidBattleInfo
enums:    SoloRaidChallengeType / StyleRentalUsingStatus / SoloRaidRoomResult
```

`check_protocol_compatibility()` 返回缺失项的 `"kind.name"` 列表，模块据此抛
`AbortError` 并列出缺了什么、当前协议版本是多少。加接口时记得同步往
`_REQUIRED_PROTOCOL` 里补。

## 错误处理

异常分工沿用项目既有约定，模块层只处理这三类：

| 异常 | 处理 |
|---|---|
| `VersionUpdatedException` | 转 `SkipError`，提示重新运行（协议刚更新完，重新登录后重放即可） |
| `NetworkException` | 转 `AbortError`，提示稍后重试 |
| `ApiException` | 记录 `result_code` 后中断本轮循环 |

其余重试由框架层负责：`misc.errorhandler` 重试 `NetworkException`，
`sessionmgr.request` 捕获 `VersionUpdatedException` 后重新登录并重放请求。

注意 `CancelledError` 继承自 `BaseException`，模块的 `except Exception` 接不住；
而 `apiclient.py` 里有一个裸 `except:` 会把它转成 `NetworkException`。排查超时问题时
要留意这条路径——大版本更新后的首次请求如果触发协议热更新，会在请求内部同步跑十几分钟，
超过前端 600 秒超时后请求被取消。这种情况应该先用独立进程跑 `python _version_update.py`，
让协议更新不发生在 Web 请求里。

## 配套功能：隐藏队伍

同页还有一个「隐藏队伍」模块，用来关掉排行榜里的队伍详情公开，避免别人点进结算记录
就看到出战队伍。

抓包对应 `/api/user/save_option`，payload 的 42 个字段里有三个控制展示：

| 字段 | 含义 |
|---|---|
| `characterBuildDetailPublishSoloRaid` | 总力战 |
| `characterBuildDetailPublishMultiRaid` | 团战 |
| `characterBuildDetailPublishScoreAttack` | 打分 |

**这个接口是整体替换，不是局部更新。** `apiclient` 序列化用的是
`req.dict(by_alias=True)`，没有 `exclude_none`，只提交三个字段会把其余设置全部写成
`null`。所以流程必须是：`UserApiLoadOptionRequest` 读回全量配置 → 只翻转这三个开关 →
`UserApiSaveOptionRequest` 整体写回。

`sm` 与 `lastHomeAccessTime` 是 `RequestBase` 上的字段，由 `apiclient` 自动填充，
不要手动传。

总力战始终关闭，团战与打分各有一个开关（默认都开）。

## 风险与边界

- 本功能在**危险**页，默认关闭，需要在界面上手动开启。
- `simulate` / `minimal` 提交的是自制日志，**依赖服务端不校验日志真实性**。
  服务端一旦加强校验，这两条路会失效，甚至可能带来账号风险，请自行评估。
- `skip` 走官方接口，风险最低，但要求该难度已通关过一次。
- 生成器只保证"结构合法 + 伤害足以击杀"，不保证与真实战斗过程一致。
- 战力门槛是**自己加的自律规则**，不是游戏限制。服务端不会因为战力低而拒绝结算；
  门槛只是为了别让结算记录太扎眼。要改阈值改 `MIN_PARTY_POWER` 即可。
- 主数据里的防御力字段是 `_def`（`alias='def'`），pydantic v1 会把下划线开头的字段
  当私有属性，`dict()` 里取不到。取值统一走 `_safe_int(getattr(x, "_def", 0))` 容错，
  取不到就按 0 算。

## 测试

离线测试不依赖网络与账号：

```powershell
python -m unittest discover -s tests -p "test_soloraid_battlelog.py" -v
python -m unittest discover -s tests -p "test_hide_party.py" -v
```

- `test_soloraid_battlelog.py`：斩杀时机与回合数、伤害是否致命、终局单位状态、
  指令结构、`battleInfo` 终局标记、极简模式、builder 复用同一批单位对象时是否互相污染。
- `test_hide_party.py`：`save_option` 必须整体写回（含"只发一个字段会把其余 39 个
  写成 `null`"的反例）、开关翻转与字段保留、战力门槛边界值（刚好达标通过、差 1 点拒绝）、
  战力的「万」显示与退化格式、队伍战力读取的容错、难度选项标注文案。

`skip` 与完整流程需要真实账号，只能实机验证。
