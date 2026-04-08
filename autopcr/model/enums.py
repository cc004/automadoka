from enum import IntEnum

class FriendFriendType(IntEnum):
    None_ = 0
    Follow = 1
    Followed = 2
    Friend = 3
    Block = 4
    Blocked = 5
    CrossBlock = 6

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

class StyleRentalContentId(IntEnum):
    Exploration = 1
    SoloRaid = 2

class StyleRentalRole(IntEnum):
    All = 0
    Attacker = 1
    Breaker = 2
    Healer = 3
    Buffer = 4
    Debuffer = 5
    Defender = 6

class MultiRaidRoomResult(IntEnum):
    Init = -1
    None_ = 0
    Win = 1
    LoseForRoundLimit = 2
    LoseForDead = 3
    Timeout = 4
    Retire = 5

class HomeDispBalloonType(IntEnum):
    Exploration = 1
    AlternativeStory = 2

class GachaGachaType(IntEnum):
    Normal = 1
    StepUp = 2
    StartDash = 3
    Comeback = 4
    Tutorial = 5
    Bonus = 6

class GachaGachaDrawType(IntEnum):
    Normal = 1
    StepUp = 2
    Tutorial = 3

class FriendSortCondition(IntEnum):
    Level = 0
    MaxPartyPower = 1
    RecentLoginTime = 2

class FriendSortOrder(IntEnum):
    SortAsc = 0
    SortDesc = 1

class CollectionAdvSkipType(IntEnum):
    None_ = 0
    Normal = 1
    Fast = 2
    Skip = 3

