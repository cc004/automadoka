from enum import IntEnum

class FriendFriendType(IntEnum):
    None_ = 0
    Follow = 1
    Followed = 2
    Friend = 3
    Block = 4
    Blocked = 5
    CrossBlock = 6

class SnsPostType(IntEnum):
    None_ = 0
    Profile = 1

class SelectionAbilityLockType(IntEnum):
    None_ = 0
    Temporary = 1
    Permanent = 2

class QuestOutGameEnemyUnlockType(IntEnum):
    None_ = 1
    MiniTutorialNum = 2

class ExplorationAdvPlayType(IntEnum):
    TwoDimensional = 1
    ThreeDimensional = 2
    Movie = 3

class LoginBonusCycleType(IntEnum):
    Loop = 1
    NoLoop = 2
    Comeback = 3
    SubscriptionRegular = 4
    SubscriptionPremium = 5
    IndividualLottery = 6

class QuestOutGameLinkHpType(IntEnum):
    None_ = 0
    NormalLink = 1
    BossLink = 2

class LotteryLotteryType(IntEnum):
    Normal = 0
    Mini = 1

class LotteryConditionType(IntEnum):
    NotMatch = 0
    MatchLowDigit = 1
    MatchAll = 2

class AlternativeStoryPointType(IntEnum):
    Quest = 1
    Adv = 2
    Sequence = 3

class AlternativeStoryStoryType(IntEnum):
    BlackMemoryLight = 1
    AlternativeStory = 2

class AlternativeStoryBgAnimType(IntEnum):
    ToLarge = 1
    ToSmall = 2
    ToRight = 3
    ToLeft = 4

class AlternativeStorySequenceType(IntEnum):
    Quest = 1
    Adv = 2

class CollaborationTargetObjectType(IntEnum):
    Title = 1
    Model3d = 2
    Live2d = 3
    Dollhouse3dBackground = 4
    Dollhouse2dBackground = 5
    Character = 6

class BattleRoleType(IntEnum):
    Attacker = 1
    Breaker = 2
    Healer = 3
    Buffer = 4
    Debuffer = 5
    Defender = 6

class MissionTransitionType(IntEnum):
    None_ = 0
    ByQuestStageMstId = 1
    ByQuestMapMstId = 2
    ByQuestCategoryMstId = 3
    ByQuestGroupMstId = 4
    ByFieldStageMstId = 5
    TrainingStyle = 6
    TrainingCard = 7
    Pvp = 8
    EnhanceQuest = 9
    Profile = 10
    Guild = 11
    CharacterHeartGallery = 12
    Gacha = 13
    Party = 14
    ScoreAttackByScoreAttackMstId = 15
    MultiRaid = 16
    SoloRaid = 17
    AlternativeStory = 18

class ObjectObjectType(IntEnum):
    Gem = 1
    Card = 2
    Item = 3
    Character = 4
    Style = 5
    Adv = 6
    Gold = 7
    Talisman = 8
    Enemy = 9
    DioramaBackground = 10
    ChargeGem = 11
    UserTitle = 12
    Sound = 13
    UserExp = 14
    Dollhouse3dBackground = 15
    Dollhouse2dBackground = 16
    StyleLive2dCostume = 17
    Style3dCharacter = 18
    WishlistSlot = 19
    KiokuHikari = 999

class StyleRentalUsingStatus(IntEnum):
    NotUsing = 0
    Using = 1
    AutoUsing = 2

class QuestBattleResult(IntEnum):
    Init = -1
    None_ = 0
    Win = 1
    Lose = 2
    Timeout = 3
    Retire = 4
    Skip = 5

class StyleRentalContentId(IntEnum):
    Exploration = 1
    SoloRaid = 2
    MultiRaid = 3

class StyleRentalRole(IntEnum):
    All = 0
    Attacker = 1
    Breaker = 2
    Healer = 3
    Buffer = 4
    Debuffer = 5
    Defender = 6

class DailySkipDailyClearType(IntEnum):
    EventQuest = 1
    ScoreAttack = 2
    EventArchive = 3
    TrainingQuest = 4
    CharacterHeartQuest = 5
    GatheringShortcutQuest = 6
    GatheringReward = 7

class SoloRaidRoomResult(IntEnum):
    Init = -1
    None_ = 0
    Win = 1
    LoseForRoundLimit = 2
    LoseForDead = 3
    Withdraw = 4
    Timeout = 5
    Retire = 6
    Retry = 7
    Skip = 8

class SoloRaidChallengeType(IntEnum):
    Normal = 1
    Practice = 2

class SoloRaidStageResult(IntEnum):
    Playing = 0
    Win = 1
    Lose = 2

class SelectionAbilitySubRarityGroup(IntEnum):
    B = 1
    A = 2
    S = 3

class UserProfileDisplayItemType(IntEnum):
    None_ = 0
    FavoriteCharacter = 1
    SoloRaidHighestRank = 2
    ScoreAttackHighestRank = 3
    TrophyCount = 4
    CollectionAchievedLevel = 5
    PvpHighestRank = 6
    PartyMaxPower = 7
    AcquiredStyleNum = 8
    StartDatetime = 9
    MultiRaidLikeCount = 10

class DollhouseRandomScopeType(IntEnum):
    All = 1
    Configured = 2

class MultiRaidRoomResult(IntEnum):
    Init = -1
    None_ = 0
    Win = 1
    LoseForRoundLimit = 2
    LoseForDead = 3
    Timeout = 4
    Retire = 5

class GemRewardTabType(IntEnum):
    None_ = 0
    Standing = 1
    Limited = 2

class GemRewardContentType(IntEnum):
    None_ = 0
    Exploration = 1
    Collection = 2
    AlternativeStory = 3
    StoryEvent = 4
    ShopSeries = 5
    StoryEventArchive = 6
    MultiRaid = 7
    Tower = 8
    StyleTraining = 9
    StyleParamUpTraining = 10
    SelectionAbilityTraining = 11
    CharacterHeart = 12
    CollectionFirstView = 13

class TransitionTransitionType(IntEnum):
    None_ = 0
    ByFieldStageMstId = 100
    ByFieldPointMstId = 101
    ByAlternativeStoryMstId = 110
    ByAlternativeStoryPointMstId = 111
    ByStoryEventMstId = 120
    ByStoryEventQuestStageMstId = 121
    StyleTrainingTop = 200
    StyleParamUpTrainingTop = 201
    SelectionAbilityTrainingTop = 210
    CharacterHeartTop = 220
    MultiRaidTop = 300
    TowerTop = 310
    ByTowerQuestStageMstId = 311
    ByShopSeriesMstId = 400
    CollectionFirstViewTop = 500

class HomeDispBalloonType(IntEnum):
    Exploration = 1
    AlternativeStory = 2
    AlternativeStoryPointGroup = 3

class GachaGachaType(IntEnum):
    Normal = 1
    StepUp = 2
    StartDash = 3
    Comeback = 4
    Tutorial = 5
    Bonus = 6
    WishlistNormal = 8
    WishlistStepUp = 9

class GachaGachaDrawType(IntEnum):
    Normal = 1
    StepUp = 2
    Tutorial = 3
    WishlistNormal = 5
    WishlistStepUp = 6

class FriendSortCondition(IntEnum):
    Level = 0
    MaxPartyPower = 1
    RecentLoginTime = 2

class FriendSortOrder(IntEnum):
    SortAsc = 0
    SortDesc = 1

class QuestOutGamePlayType(IntEnum):
    roundEnd = 1
    battleStart = 2

class CollectionAdvSkipType(IntEnum):
    None_ = 0
    Normal = 1
    Fast = 2
    Skip = 3

