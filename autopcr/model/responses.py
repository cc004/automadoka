from typing import List, Dict
from .modelbase import ResponseBase
from .common import *
from .enums import *
from pydantic import Field

class WebPlayApiLoginLogResponse(ResponseBase):
    isSuccess: bool = None
class WebPlayApiGetUserMigrationInfoResponse(ResponseBase):
    platform: int = None
    uniqueId: str = None
    xuid: str = None
    userVerify: str = None
class WebPayApiPurchaseResponse(ResponseBase):
    result: str = None
    url: str = None
    purchaseId: str = None
    code: int = None
    message: str = None
class WebPayApiGetPurchaseResultResponse(ResponseBase):
    purchase: WebPayPurchaseResultRecord = None
class WebPayApiRestoreResponse(ResponseBase):
    result: str = None
    code: int = None
    message: str = None
class WebPayApiCancelLatestResponse(ResponseBase):
    result: str = None
class TitleApiGetTitleTopDataResponse(ResponseBase):
    viewData: TitleTitleViewData = None
    privacyUrl: str = None
class TermsApiGetUpdatedTermsResponse(ResponseBase):
    needAgree: bool = None
    termsList: List[TermsTermsInfo] = None
class TermsApiAgreeLatestTermsResponse(ResponseBase):
    needAgree: bool = None
class TermsApiAgreeChatTermsResponse(ResponseBase):
    userData: UserUserDataRecord = None
class TalismanApiGetTalismanListResponse(ResponseBase):
    talismanDataList: List[TalismanTalismanDataRecord] = None
class TalismanApiTalismanLevelUpResponse(ResponseBase):
    talismanData: TalismanTalismanDataRecord = None
    deletedTalismanDataIds: List[int] = None
    userParamData: UserUserParamDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class TalismanApiTalismanSellResponse(ResponseBase):
    deletedTalismanDataIds: List[int] = None
    userParamData: UserUserParamDataRecord = None
class TalismanApiSetTalismanProtectResponse(ResponseBase):
    talismanData: TalismanTalismanDataRecord = None
class ServerApiGetTimeZoneInfoResponse(ResponseBase):
    timezone: str = None
    offsetSeconds: int = None
class ServerApiCertHashListResponse(ResponseBase):
    sslHashList: List[str] = None
class SerialCampaignApiInputSerialCodeResponse(ResponseBase):
    viewText: str = None
class SerialCampaignApiPreAppLinkResponse(ResponseBase):
    viewText: str = None
class SampleApiHttpConnectResponse(ResponseBase):
    replyText: str = None
class NotificationApiRegisterResponse(ResponseBase):
    result: bool = None
class NotificationApiSetOsResponse(ResponseBase):
    result: bool = None
class NotificationApiSetLanguageResponse(ResponseBase):
    result: bool = None
class NotificationApiSetRegionResponse(ResponseBase):
    result: bool = None
class NotificationApiSetTimezoneResponse(ResponseBase):
    result: bool = None
class NotificationApiUnsetOsResponse(ResponseBase):
    result: bool = None
class NotificationApiUnsetRegionResponse(ResponseBase):
    result: bool = None
class NotificationApiUnsetLanguageResponse(ResponseBase):
    result: bool = None
class NotificationApiUnsetTimezoneResponse(ResponseBase):
    result: bool = None
class NotificationApiSetTagResponse(ResponseBase):
    result: bool = None
class NotificationApiUnsetTagResponse(ResponseBase):
    result: bool = None
class MapGveApiGetTopInfoResponse(ResponseBase):
    userParamData: UserUserParamDataRecord = None
    mapGveUserData: MapGveMapGveUserDataRecord = None
    mapGveGuildData: MapGveMapGveGuildDataRecord = None
    rankingInfo: List[MapGveMapGveRankingRecord] = None
class MapGveApiReachPointResponse(ResponseBase):
    mapGveUserData: MapGveMapGveUserDataRecord = None
    mapGveGuildData: MapGveMapGveGuildDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
class LoginApiLoginResponse(ResponseBase):
    sessionId: str = None
    userId: int = None
    status: int = None
    banType: int = None
class LikeApiExecLikeResponse(ResponseBase):
    result: bool = None
class InAppSnsApiCreateLoginUrlResponse(ResponseBase):
    url: str = None
    state: str = None
class InAppSnsApiGetAccessTokenResponse(ResponseBase):
    token: InAppSnsAccessToken = None
class HariboteChatApiGetMessageDataListResponse(ResponseBase):
    messageDataList: List[HariboteChatMessageDataRecord] = None
class HariboteChatApiSendMessageResponse(ResponseBase):
    messageData: HariboteChatMessageDataRecord = None
class FirestoreApiCreateTokenResponse(ResponseBase):
    token: str = None
class ExplorationBattleApiInitializeStageV4Response(ResponseBase):
    initializeStatus: int = None
    questRoomData: QuestBattleQuestRoomData = None
    isFirstBattle: bool = None
    partyDataList: List[PartyPartyDataRecord] = None
class ExplorationBattleApiFinalizeStageForUserV4Response(ResponseBase):
    result: QuestBattleResult = None
    beforeLevel: int = None
    afterLevel: int = None
    beforeExp: int = None
    afterExp: int = None
    beforeStamina: int = None
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    acquiredOtherCollectionQuestRewardMstIds: List[int] = None
    acquiredInBattleRewardAdvMstId: int = None
    canReplay: bool = None
    remainPlayCount: int = None
    objectDataRecord: ObjectObjectDataRecord = None
    keyItemDataList: List[ItemItemDataRecord] = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    styleLevelUpInfoList: List[StyleStyleLevelUpInfo] = None
    partyDataList: List[PartyPartyDataRecord] = None
    achievedConditionGroupIds: List[int] = None
    fieldStageCollectionInfo: CollectionFieldStageCollectionInfo = None
    featureReleaseList: List[TutorialFeatureRelease] = None
    nextBattleQuestStageMstId: int = None
    nextBattleFieldPointMstId: int = None
    isFirstClear: bool = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
    isStoreReview: bool = None
    acquiredRewardMoney: int = None
    userQuestMissionDataList: List[QuestOutGameUserQuestMissionDataRecord] = None
    questMissionInfoList: List[ExplorationBattleQuestMissionInfo] = None
    isUserExpStoredMessage: bool = None
class ExplorationBattleApiGetExplorationInfoResponse(ResponseBase):
    stageInfo: ExplorationBattleStageInfo = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
class ExplorationBattleApiRetireResponse(ResponseBase):
    isSuccess: bool = None
class DebugUserApiRecoverStaminaResponse(ResponseBase):
    isSuccess: bool = None
class DebugSubscriptionApiIsValidSubscriptionResponse(ResponseBase):
    isValid: bool = None
class DebugSubscriptionApiDoSubscribeForceResponse(ResponseBase):
    isSuccess: bool = None
class AppVersionApiGetReviewVersionDataResponse(ResponseBase):
    isReviewVersion: bool = None
    appealTitleInfo: AppVersionAppealTitleInfo = None
class AkamaiApiCreateTokenResponse(ResponseBase):
    token: str = None
class TowerApiGetTowerTopResponse(ResponseBase):
    userTowerData: TowerUserTowerDataRecord = None
    skipFloorData: TowerSkipFloorDataRecord = None
    userQuestStageDataList: List[QuestOutGameUserQuestStageDataRecord] = None
    objectDataRecord: ObjectObjectDataRecord = None
class TowerApiRecoverySkipNumResponse(ResponseBase):
    itemDataList: List[ItemItemDataRecord] = None
    userTowerData: TowerUserTowerDataRecord = None
class TowerApiSkipQuestBattleResponse(ResponseBase):
    result: QuestBattleResult = None
    beforeLevel: int = None
    afterLevel: int = None
    beforeExp: int = None
    afterExp: int = None
    beforeStamina: int = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    canReplay: bool = None
    remainPlayCount: int = None
    objectDataRecord: ObjectObjectDataRecord = None
    keyItemDataList: List[ItemItemDataRecord] = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    styleLevelUpInfoList: List[StyleStyleLevelUpInfo] = None
    partyDataList: List[PartyPartyDataRecord] = None
    userTowerData: TowerUserTowerDataRecord = None
    acquiredRewardMoney: int = None
class StyleApiGetStyleDataListResponse(ResponseBase):
    styleDataList: List[StyleStyleDataRecord] = None
class StyleApiStyleLevelUpResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    styleLevelUpInfo: StyleStyleLevelUpInfo = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class StyleApiStyleLevelUpVer2Response(ResponseBase):
    styleData: StyleStyleDataRecord = None
    styleLevelUpInfo: StyleStyleLevelUpInfo = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class StyleApiStyleSkillLevelUpResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class StyleApiStyleSpecialAttackSkillLevelUpResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class StyleApiStyleLimitBreakResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
class StyleApiOpenStyleParamUpTreeResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class StyleApiStyleParamUpResponse(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class StyleApiStyleParamUpVer2Response(ResponseBase):
    styleData: StyleStyleDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class StyleApiUpdateAlreadyViewResponse(ResponseBase):
    styleDataList: List[StyleStyleDataRecord] = None
class StoryEventApiGetTopResponse(ResponseBase):
    storyEventDataList: List[StoryEventStoryEventDataRecord] = None
    storyEventInfoList: List[StoryEventStoryEventInfo] = None
    questStageMstIdList: List[int] = None
    userQuestStageDataList: List[QuestOutGameUserQuestStageDataRecord] = None
    userQuestGroupOpenDataList: List[QuestOutGameUserQuestGroupDataRecord] = None
    storyEventScenarioMstIdList: List[int] = None
    clearStoryEventScenarioMstIdList: List[int] = None
    scoreAttackMstIdList: List[int] = None
    userScoreAttackDataList: List[ScoreAttackUserScoreAttackDataRecord] = None
    enableEventMissionBadge: bool = None
class StoryEventApiGetArchiveEventListResponse(ResponseBase):
    storyEventDataList: List[StoryEventStoryEventDataRecord] = None
    storyEventInfoList: List[StoryEventStoryEventInfo] = None
    questStageMstIdList: List[int] = None
    userQuestStageDataList: List[QuestOutGameUserQuestStageDataRecord] = None
    userQuestGroupOpenDataList: List[QuestOutGameUserQuestGroupDataRecord] = None
    storyEventScenarioMstIdList: List[int] = None
    clearStoryEventScenarioMstIdList: List[int] = None
class StoryEventApiOpenStoryResponse(ResponseBase):
    userQuestGroupOpenDataList: List[QuestOutGameUserQuestGroupDataRecord] = None
    itemDataList: List[ItemItemDataRecord] = None
class StoryEventApiScenarioReadResponse(ResponseBase):
    objectDataRecord: ObjectObjectDataRecord = None
class StoryEventApiRecoverPlayableCountResponse(ResponseBase):
    storyEventData: StoryEventStoryEventDataRecord = None
class ShopApiGetShopListResponse(ResponseBase):
    shopCountDataList: List[ShopShopCountDataRecord] = None
class ShopApiBuyResponse(ResponseBase):
    viewData: ShopBuyViewData = None
    shopCountData: ShopShopCountDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
    receivedObjectDataList: List[ShopReceivedObjectData] = None
    partyDataList: List[PartyPartyDataRecord] = None
class ShopApiGetShopPaymentMstListResponse(ResponseBase):
    shopPaymentMstList: List[ShopShopPaymentMstRecord] = None
    shopPaymentBonusRewardMstList: List[ShopShopPaymentBonusRewardMstRecord] = None
    isDisplayWebShopButton: bool = None
    subscriptionDescriptionList: List[ShopSubscriptionDescriptionRecord] = None
class SelectionAbilityApiGetSelectionAbilityDataListResponse(ResponseBase):
    selectionAbilityDataList: List[SelectionAbilitySelectionAbilityDataRecord] = None
class SelectionAbilityApiDeleteSelectionAbilityResponse(ResponseBase):
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class SelectionAbilityApiLearnSubSelectionAbilityResponse(ResponseBase):
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    styleData: StyleStyleDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class SelectionAbilityApiSetSelectionAbilityResponse(ResponseBase):
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    styleData: StyleStyleDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class SelectionAbilityApiEnableMainSelectionAbilityResponse(ResponseBase):
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class SelectionAbilityApiLearnMainSelectionAbilityUseItemResponse(ResponseBase):
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    learnSelectionAbilityMstIds: List[int] = None
    selectionAbilityConversionItemDataList: List[SelectionAbilitySelectionAbilityConversionItemData] = None
class ScoreAttackApiGetScoreAttackTopResponse(ResponseBase):
    selfRanking: int = None
    userScoreAttackData: ScoreAttackUserScoreAttackDataRecord = None
class ScoreAttackApiGetRankingInfoResponse(ResponseBase):
    selfRanking: int = None
    rankingInfoList: List[ScoreAttackRankingInfo] = None
    userScoreAttackData: ScoreAttackUserScoreAttackDataRecord = None
class ScoreAttackApiInitializeStageResponse(ResponseBase):
    initializeStatus: int = None
    scoreAttackRoomData: ScoreAttackScoreAttackRoomData = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class ScoreAttackApiGetScoreAttackInfoResponse(ResponseBase):
    stageInfo: ScoreAttackStageInfo = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
class ScoreAttackApiFinalizeStageForUserResponse(ResponseBase):
    result: QuestBattleResult = None
    questStageMstId: int = None
    scoreInfo: ScoreAttackScoreInfo = None
    isHighScoreUpdated: bool = None
    selfRanking: int = None
    beforeUserScoreAttackData: ScoreAttackUserScoreAttackDataRecord = None
    afterUserScoreAttackData: ScoreAttackUserScoreAttackDataRecord = None
    acquiredScoreAttackHighScoreRewardMstIds: List[int] = None
    acquiredScoreAttackTotalScoreRewardMstIds: List[int] = None
    objectDataRecord: ObjectObjectDataRecord = None
    partyData: PartyPartyDataRecord = None
class ScoreAttackApiRetireResponse(ResponseBase):
    isSuccess: bool = None
class ScoreAttackApiGetRankingUserCharacterBuildDetailResponse(ResponseBase):
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class PvpApiGetPvpTopResponse(ResponseBase):
    pvpTopInfo: PvpPvpTopInfo = None
class PvpApiGetRankingInfoResponse(ResponseBase):
    mode: int = None
    selfRanking: int = None
    rankingInfoList: List[PvpRankingInfo] = None
class PvpApiGetCandidateEnemyUserListResponse(ResponseBase):
    selfUserInfo: PvpPvpUserInfo = None
    candidateEnemyUserInfoList: List[PvpPvpUserInfo] = None
    remainRechooseCount: int = None
class PvpApiGetEnemyUserInfoResponse(ResponseBase):
    enemyUserInfo: PvpPvpUserInfo = None
    leaderStyleMstId: int = None
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class PvpApiInitializeStageResponse(ResponseBase):
    roomId: str = None
class PvpApiRetireResponse(ResponseBase):
    isSuccess: bool = None
class PvpApiGetPvpInfoResponse(ResponseBase):
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    enemyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    enemyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    limitSecond: int = None
class PvpApiFinalizeStageResponse(ResponseBase):
    isSuccess: bool = None
class PvpApiFinalizeStageForUserResponse(ResponseBase):
    addBasePvpPoint: int = None
    addBonusPvpPoint: int = None
    addRelativelyBonusPoint: int = None
    addBattleTurnBonusPoint: int = None
    addAliveBonusPoint: int = None
    addWinStreakBonusPoint: int = None
    pointInfo: PvpPointInfo = None
    relativelyLevel: int = None
    resultRound: int = None
    aliveCount: int = None
    afterPvpPoint: int = None
    winStreakCount: int = None
    beforeRanking: int = None
    afterRanking: int = None
    leastNextRewardPoint: int = None
    pointRewardList: List[PvpRewardInfo] = None
class PvpApiGetMatchHistoryResponse(ResponseBase):
    matchHistoryList: List[PvpMatchHistory] = None
class PvpApiGetMatchDetailHistoryResponse(ResponseBase):
    matchHistory: PvpMatchHistory = None
    offenseCharacterBuildInfoList: List[PvpCharacterBuildInfo] = None
    defenseCharacterBuildInfoList: List[PvpCharacterBuildInfo] = None
class PvpApiGetMatchCharacterBuildDetailResponse(ResponseBase):
    leaderStyleMstId: int = None
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class PvpApiGetRankingUserCharacterBuildDetailResponse(ResponseBase):
    leaderStyleMstId: int = None
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class UserTitleApiGetUserTitleDataListResponse(ResponseBase):
    userTitleDataList: List[UserTitleUserTitleDataRecord] = None
class UserApiGetUserDataResponse(ResponseBase):
    userData: UserUserDataRecord = None
class UserApiGetUserParamDataResponse(ResponseBase):
    userParamData: UserUserParamDataRecord = None
class UserApiGetInitDataListResponse(ResponseBase):
    cardDataList: List[CardCardDataRecord] = None
    characterBuildDataList: List[PartyCharacterBuildDataRecord] = None
    characterDataList: List[CharacterCharacterDataRecord] = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
    styleDataList: List[StyleStyleDataRecord] = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
    userParamData: UserUserParamDataRecord = None
    userData: UserUserDataRecord = None
class UserApiGetUserProfileDataResponse(ResponseBase):
    userProfileData: UserUserProfileDataRecord = None
    playerId: str = None
    createdTime: str = None
class UserApiGetOtherUserProfileDataResponse(ResponseBase):
    otherUserParamData: UserUserParamDataRecord = None
    otherUserProfileData: UserUserProfileDataRecord = None
    otherUserPlayerId: str = None
    useCharacterRankingList: List[CharacterUseCharacterRankingRecord] = None
    altogetherMissionNum: int = None
    characterNum: int = None
    styleNum: int = None
    pvpRank: int = None
    guildData: GuildGuildDataRecord = None
    guildRequestData: GuildGuildRequestDataRecord = None
    otherPartyData: PartyPartyDataRecord = None
    otherCharacterBuildDataList: List[PartyCharacterBuildDataRecord] = None
    otherCharacterDataList: List[CharacterCharacterDataRecord] = None
    otherStyleDataList: List[StyleStyleDataRecord] = None
    otherCardDataList: List[CardCardDataRecord] = None
    otherTalismanDataList: List[TalismanTalismanDataRecord] = None
    otherCollectionParamUpAchieveData: CollectionCollectionParamUpAchieveDataRecord = None
    createdTime: str = None
class UserApiSetNameResponse(ResponseBase):
    userParamData: UserUserParamDataRecord = None
class UserApiSetCommentResponse(ResponseBase):
    userProfileData: UserUserProfileDataRecord = None
class UserApiSetFavoriteInfoResponse(ResponseBase):
    userProfileData: UserUserProfileDataRecord = None
    userParamData: UserUserParamDataRecord = None
class UserApiSetDisplayUserTitleResponse(ResponseBase):
    userProfileData: UserUserProfileDataRecord = None
    userParamData: UserUserParamDataRecord = None
class UserApiSetStaminaRecoverResponse(ResponseBase):
    userParamData: UserUserParamDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class UserApiSaveOptionResponse(ResponseBase):
    isSuccess: bool = None
class UserApiLoadOptionResponse(ResponseBase):
    paymentAlert: bool = None
    battleDirectionSkip: bool = None
    battleActionTimeView: bool = None
    savedOnce: bool = None
    sameCharaOnParty: bool = None
    battleSpeedType: int = None
    battleAuto: int = None
    bgmSwitchType: int = None
    questPartyDataId: int = None
    pvpPartyDataId: int = None
    characterHeartPartyDataId: int = None
    characterHeartUnlockNormalStageMstId: int = None
    characterHeartUnlockNightmareStageMstId: int = None
    characterHeartLastPlayedStageMstId: int = None
    notShowTodayHomeAppeal: bool = None
    characterTalkAutoStateIndex: int = None
    advIsAuto: bool = None
    advFastAutoIndex: int = None
    dungeonIsFast: bool = None
    dungeonIsManual: bool = None
    confirmWalpurgisAttentionPopup: bool = None
    homeAppealLocalInfo: List[UserHomeAppealLocalInfo] = None
    enhanceQuestUserLocalInfo: UserEnhanceQuestUserLocalInfo = None
    mainQuestUserLocalInfo: UserMainQuestUserLocalInfo = None
    storyEventLocalInfo: List[UserStoryEventLocalInfo] = None
    sortInfo: List[UserSortInfo] = None
    sortDescInfo: List[UserSortDescInfo] = None
    filterInfo: List[UserFilterInfo] = None
class UserApiUserSearchResponse(ResponseBase):
    userParamDataList: List[UserUserParamDataRecord] = None
    userProfileDataList: List[UserUserProfileDataRecord] = None
    userDisplayInfoList: List[UserUserDisplayInfo] = None
class UserApiGetUserSubscriptionDataResponse(ResponseBase):
    userSubscriptionDataList: List[UserUserSubscriptionDataRecord] = None
class UserApiGetUserDisplayInfoListResponse(ResponseBase):
    userDisplayInfoList: List[UserUserDisplayInfo] = None
class UserApiInitConfigResponse(ResponseBase):
    isSuccess: bool = None
class UserApiAccountDeleteResponse(ResponseBase):
    isSuccess: bool = None
class UserApiStoreReviewResponse(ResponseBase):
    isSuccess: bool = None
class UserApiGetPlayerIdResponse(ResponseBase):
    playerId: str = None
class PresentApiGetPresentDataListResponse(ResponseBase):
    presentDataList: List[PresentPresentDataRecord] = None
class PresentApiGetReceivedHistoryResponse(ResponseBase):
    presentDataList: List[PresentPresentDataRecord] = None
class PresentApiGetNoReceivedPresentNumResponse(ResponseBase):
    num: int = None
class PresentApiReceiveResponse(ResponseBase):
    expireTimeOverNum: int = None
    receivedPresentDataList: List[PresentPresentDataRecord] = None
    objectDataRecord: ObjectObjectDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class MultiRaidApiGetTopResponse(ResponseBase):
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
    multiRaidStageDataList: List[MultiRaidMultiRaidStageDataRecord] = None
    multiRaidRoomDataList: List[MultiRaidMultiRaidRoomDataRecord] = None
    userLikeData: UserUserLikeDataRecord = None
    enableMissionBadge: bool = None
class MultiRaidApiGetMultiRaidStageDataListResponse(ResponseBase):
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
    multiRaidStageDataList: List[MultiRaidMultiRaidStageDataRecord] = None
    multiRaidRoomDataList: List[MultiRaidMultiRaidRoomDataRecord] = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
class MultiRaidApiInitializeStageResponse(ResponseBase):
    initializeStatus: int = None
    multiRaidStageData: MultiRaidMultiRaidStageDataRecord = None
    multiRaidRoomData: MultiRaidMultiRaidRoomDataRecord = None
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class MultiRaidApiFinalizeStageForUserResponse(ResponseBase):
    result: MultiRaidRoomResult = None
    score: int = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
    rewardInfo: MultiRaidRewardInfo = None
    multiRaidStageData: MultiRaidMultiRaidStageDataRecord = None
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
class MultiRaidApiGetMultiRaidInfoResponse(ResponseBase):
    stageInfo: QuestBattleStageInfo = None
    multiRaidRoomData: MultiRaidMultiRaidRoomDataRecord = None
    multiRaidStageData: MultiRaidMultiRaidStageDataRecord = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
class MultiRaidApiSendRescueResponse(ResponseBase):
    result: bool = None
class MultiRaidApiRetireResponse(ResponseBase):
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
class MultiRaidApiRecoverStaminaResponse(ResponseBase):
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class MultiRaidApiAddDamageResponse(ResponseBase):
    hp: int = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
class MultiRaidApiSyncBattleInfoResponse(ResponseBase):
    hp: int = None
    damage: int = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
class MultiRaidApiReceiveRewardResponse(ResponseBase):
    result: MultiRaidRoomResult = None
    score: int = None
    joinUserInfoList: List[MultiRaidJoinUserInfo] = None
    rewardInfo: MultiRaidRewardInfo = None
    multiRaidStageData: MultiRaidMultiRaidStageDataRecord = None
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidUserSeasonData: MultiRaidMultiRaidUserSeasonDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
class MissionApiGetMissionDataListResponse(ResponseBase):
    currentMissionTitleMstId: int = None
    missionDataList: List[MissionMissionDataRecord] = None
    enableSubscriptionLabel: List[str] = None
    rewardReceivableMissionTypeList: List[int] = None
    guildMissionDataList: List[GuildMissionGuildMissionDataRecord] = None
    guildUserData: GuildGuildUserDataRecord = None
    enableComebackButton: bool = None
class MissionApiReceiveResponse(ResponseBase):
    missionDataList: List[MissionMissionDataRecord] = None
    objectDataRecord: ObjectObjectDataRecord = None
    receivedObjectDataList: List[MissionreceivedObjectData] = None
    currentMissionTitleMstId: int = None
    partyDataList: List[PartyPartyDataRecord] = None
    rewardReceivableMissionTypeList: List[int] = None
class TutorialApiUpdateTutorialStepResponse(ResponseBase):
    objectDataRecord: ObjectObjectDataRecord = None
class TutorialApiGetMiniTutorialDataResponse(ResponseBase):
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class TutorialApiExecMiniTutorialResponse(ResponseBase):
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class TutorialApiGetPrologueBattleInfoResponse(ResponseBase):
    questStageMstId: int = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
class TutorialApiSkipTutorialToGachaResponse(ResponseBase):
    objectDataRecord: ObjectObjectDataRecord = None
class ItemApiGetItemDataListResponse(ResponseBase):
    itemDataList: List[ItemItemDataRecord] = None
class ItemApiGetItemDataListByItemMstIdListResponse(ResponseBase):
    itemDataList: List[ItemItemDataRecord] = None
class ItemApiUseItemResponse(ResponseBase):
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class ItemApiSellItemResponse(ResponseBase):
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class HomeApiGetHomeInfoResponse(ResponseBase):
    viewData: HomeHomeViewData = None
    loginBonusDataList: List[HomeLoginBonusRecord] = None
    userProfileData: UserUserProfileDataRecord = None
    comebackUserData: UserComebackUserDataRecord = None
    questBattleRoomId: int = None
    backGroundPlay: bool = None
    explorationBattleRoomId: int = None
    gveRoomId: int = None
    pvpRoomId: str = None
    gvgRoomId: str = None
    scoreAttackRoomId: int = None
    multiRaidRoomId: int = None
    bonusGachaMstId: int = None
    achievedConditionGroupIds: List[int] = None
    userSubscriptionDataList: List[UserUserSubscriptionDataRecord] = None
    finishedMiniTutorialNumberList: List[int] = None
    bgmCueSheetName: str = None
    bgmCueName: str = None
    gatheringTime: str = None
    userLevelUpInfo: UserUserLevelUpInfo = None
    isUserExpStoredMessage: bool = None
    userGatheringData: GatheringUserGatheringDataRecord = None
    nextChallengeFieldStageMstId: int = None
class GvgApiGetTopResponse(ResponseBase):
    gvgGuildInfo: GvgGvgGuildInfo = None
    gvgEnemyGuildInfo: GvgGvgEnemyGuildInfo = None
    allyMatchTopInfoList: List[GvgMatchTopInfo] = None
    enemyMatchTopInfoList: List[GvgMatchTopInfo] = None
    day: int = None
    startTime: str = None
    endTime: str = None
    preLeagueStartTime: str = None
    preLeagueEndTime: str = None
    leagueStartTime: str = None
    leagueEndTime: str = None
    resourceName: str = None
    canPlayTodayBattle: bool = None
    eventStateType: int = None
class GvgApiGetMatchHistoryResponse(ResponseBase):
    matchHistoryList: List[GvgMatchHistory] = None
class GvgApiGetMatchDetailHistoryResponse(ResponseBase):
    matchHistory: GvgMatchHistory = None
    allyCharacterBuildInfoList: List[PvpCharacterBuildInfo] = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    enemyCharacterBuildInfoList: List[PvpCharacterBuildInfo] = None
    enemyBattleUnitList: List[QuestBattleBattleUnit] = None
class GvgApiGetMatchCharacterBuildDetailResponse(ResponseBase):
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class GvgApiGetCandidateEnemyUserListResponse(ResponseBase):
    enemyGuildName: str = None
    enemyGuildDataId: int = None
    enemyGuildTitleMstId: int = None
    allyAttackUserCount: int = None
    enemyAttackUserCount: int = None
    allyGuildPoint: int = None
    enemyGuildPoint: int = None
    matchInfoList: List[GvgMatchInfo] = None
    canPlayAdditionalBattle: bool = None
class GvgApiGetRankingInfoResponse(ResponseBase):
    rankingInfoList: List[GvgRankingInfo] = None
class GvgApiGetLeagueMatchResultsResponse(ResponseBase):
    leagueMatchResultsList: List[GvgLeagueMatchResultInfo] = None
    gvgGuildInfoList: List[GvgLeagueMatchGuildInfo] = None
class GvgApiGetEnemyUserInfoResponse(ResponseBase):
    enemyUserInfo: GvgMatchInfo = None
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class GvgApiGetTrialEnemyUserInfoResponse(ResponseBase):
    enemyUserInfo: GvgMatchInfo = None
    characterBuildDetailList: List[PartyCharacterBuildDetail] = None
class GvgApiInitializeStageResponse(ResponseBase):
    gvgRoomId: str = None
    stageInfo: GvgStageInfo = None
class GvgApiGetGvgInfoResponse(ResponseBase):
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    enemyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    enemyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    limitSecond: int = None
class GvgApiRetireResponse(ResponseBase):
    isSuccess: bool = None
class GvgApiGetTrialGvgInfoResponse(ResponseBase):
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    enemyBattleUnitList: List[QuestBattleBattleUnit] = None
    stageInfo: GvgStageInfo = None
class GvgApiGetTrialCandidateEnemyUserListResponse(ResponseBase):
    matchInfoList: List[GvgMatchInfo] = None
class GvgApiFinalizeStageForUserResponse(ResponseBase):
    addBasePoint: int = None
    addRelativelyBonusPoint: int = None
    addBattleTurnBonusPoint: int = None
    addAliveBonusPoint: int = None
    relativelyLevel: int = None
    resultRound: int = None
    aliveCount: int = None
    addPoint: int = None
    totalPoint: int = None
    totalGuildPoint: int = None
class GveApiGetTopResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    gveMstId: int = None
    topResourceName: str = None
class GveApiGetGuildInfoResponse(ResponseBase):
    gveGuildData: GveGveGuildDataRecord = None
    gveUserData: GveGveUserDataRecord = None
    gveStageDataList: List[GveGveStageDataRecord] = None
    gveUserStageDataList: List[GveGveUserStageDataRecord] = None
    gveGuildChainData: GveGveGuildChainDataRecord = None
class GveApiGetRankingInfoResponse(ResponseBase):
    selfRanking: int = None
    rankingInfoList: List[GveRankingInfo] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GveApiGetGveHistoryResponse(ResponseBase):
    gveHistoryList: List[GveGveHistoryInfo] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GveApiInitializeStageResponse(ResponseBase):
    hp: int = None
    questRoomData: QuestBattleQuestRoomData = None
    isChallengedFirstBattle: bool = None
    guildMemberCharacterList: List[GveGuildMemberCharacter] = None
class GveApiGetGveInfoResponse(ResponseBase):
    stageInfo: QuestBattleStageInfo = None
    gveStageData: GveGveStageDataRecord = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
class GveApiAddDamageResponse(ResponseBase):
    hp: int = None
    breakCount: int = None
    isBreakBonus: bool = None
    gveUserChainList: List[GveGveUserChainDataRecord] = None
    gveHistoryList: List[GveGveHistoryInfo] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GveApiFinalizeStageForUserResponse(ResponseBase):
    rewardMedalNum: int = None
    hp: int = None
    acquiredGveStageRewardMstIds: List[int] = None
    mapGveUserData: MapGveMapGveUserDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
class GveApiRetireResponse(ResponseBase):
    isSuccess: bool = None
class GuildApiAppointGuildSubMasterResponse(ResponseBase):
    userParamDataList: List[UserUserParamDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
class GuildApiApproveJoinRequestResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiApproveScoutResponse(ResponseBase):
    guildDataId: int = None
class GuildApiCancelJoinRequestResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiCancelScoutResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGuildNameSearchResponse(ResponseBase):
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiConditionalGuildSearchResponse(ResponseBase):
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiRecommendedGuildSearchResponse(ResponseBase):
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiCreateGuildResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    guildUserData: GuildGuildUserDataRecord = None
class GuildApiDenyJoinRequestResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiDenyScoutResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiExpelGuildMemberResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGetApplyingJoinRequestListByGuildResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGetApplyingJoinRequestListByUserResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGetApplyingScoutListByGuildResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGetApplyingScoutListByUserResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiGetGuildDataResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    guildUserDataForGuildMaster: GuildGuildUserDataRecord = None
    guildMasterUserParamData: UserUserParamDataRecord = None
    myGuildUserData: GuildGuildUserDataRecord = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
    guildRequestData: GuildGuildRequestDataRecord = None
class GuildApiGetGuildTopInfoResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
    guildTitleDataList: List[GuildGuildTitleDataRecord] = None
    applyingJoinRequestCount: int = None
    guildActivityDataList: List[GuildGuildActivityDataRecord] = None
    enableGveBadge: bool = None
    enableGveParticipationBadge: bool = None
    enableGvgBadge: bool = None
class GuildApiGetGuildMemberListResponse(ResponseBase):
    userParamDataList: List[UserUserParamDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
class GuildApiJoinRequestResponse(ResponseBase):
    autoJoined: bool = None
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiLeaveGuildResponse(ResponseBase):
    guildDataId: int = None
    guildUserData: GuildGuildUserDataRecord = None
class GuildApiMigrateGuildMasterResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    userParamDataList: List[UserUserParamDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
class GuildApiMigrateGuildSubMasterResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
    userParamDataList: List[UserUserParamDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
class GuildApiRemoveGuildResponse(ResponseBase):
    guildDataId: int = None
    guildUserData: GuildGuildUserDataRecord = None
class GuildApiRemoveGuildSubMasterResponse(ResponseBase):
    userParamDataList: List[UserUserParamDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
class GuildApiGetCandidateScoutUserListResponse(ResponseBase):
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiScoutResponse(ResponseBase):
    guildRequestDataList: List[GuildGuildRequestDataRecord] = None
    guildDataList: List[GuildGuildDataRecord] = None
    guildUserDataList: List[GuildGuildUserDataRecord] = None
    userParamDataList: List[UserUserParamDataRecord] = None
class GuildApiSetGuildBasicSettingsResponse(ResponseBase):
    guildData: GuildGuildDataRecord = None
class GuildApiInstantJoinRequestResponse(ResponseBase):
    guildDataId: int = None
class GuildApiGetGuildTitleDataListResponse(ResponseBase):
    guildTitleDataList: List[GuildGuildTitleDataRecord] = None
class GatheringApiGetGatheringTopResponse(ResponseBase):
    rewardList: List[ObjectObjectViewData] = None
    userGatheringData: GatheringUserGatheringDataRecord = None
class GatheringApiReceiveRewardResponse(ResponseBase):
    receivedRewardList: List[ObjectObjectViewData] = None
    userGatheringData: GatheringUserGatheringDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
    isUserExpStoredMessage: bool = None
class GatheringApiShortcutGatheringResponse(ResponseBase):
    receivedRewardList: List[ObjectObjectViewData] = None
    userGatheringData: GatheringUserGatheringDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
class GachaApiGetGachaTopResponse(ResponseBase):
    viewData: GachaGachaTopViewData = None
class GachaApiGachaExecResponse(ResponseBase):
    gachaCountDataList: List[GachaGachaCountDataRecord] = None
    gachaGainBonusList: List[ObjectObjectViewData] = None
    gachaSeriesGainBonusList: List[ObjectObjectViewData] = None
    gachaPickUpGainBonusList: List[ObjectObjectViewData] = None
    objectDataRecord: ObjectObjectDataRecord = None
    gachaRecord: GachaGachaRecord = None
    gachaSeriesRecord: GachaGachaSeriesRecord = None
    pickUpInfoList: List[GachaPickUpInfo] = None
    isCeilingPointAchieved: bool = None
    partyDataList: List[PartyPartyDataRecord] = None
    isStoreReview: bool = None
    bonusGachaRecord: GachaGachaRecord = None
    bonusGachaSeriesRecord: GachaGachaSeriesRecord = None
    gachaSeriesBonusList: List[GachaGachaSeriesBonusRecord] = None
    gachaPickUpBonusList: List[GachaGachaPickUpBonusRecord] = None
    candidateRarityList: List[int] = None
class GachaApiUpdateAlreadyViewResponse(ResponseBase):
    newBadgeGachaSeriesMstIdList: List[int] = None
class GachaApiGetGachaGemTextListResponse(ResponseBase):
    gachaGemTextInfoList: List[GachaGachaGemTextInfo] = None
class QuestOutGameApiGetUserQuestStageListResponse(ResponseBase):
    questStageMstIdList: List[int] = None
    userQuestStageDataList: List[QuestOutGameUserQuestStageDataRecord] = None
    userQuestGroupOpenDataList: List[QuestOutGameUserQuestGroupDataRecord] = None
class QuestOutGameApiOpenQuestGroupResponse(ResponseBase):
    userQuestGroupOpenData: QuestOutGameUserQuestGroupDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
class QuestOutGameApiGetUserTrainingQuestDataListResponse(ResponseBase):
    userQuestTrainingDataList: List[QuestOutGameUserQuestTrainingDataRecord] = None
class QuestOutGameApiSetUserTrainingQuestRankUpEffectResponse(ResponseBase):
    userQuestTrainingDataList: List[QuestOutGameUserQuestTrainingDataRecord] = None
class QuestOutGameApiGetUserQuestCharacterHeartListResponse(ResponseBase):
    userQuestCharacterHeartData: QuestOutGameUserQuestCharacterHeartDataRecord = None
    userQuestCharacterHeartPartySaveDataList: List[QuestOutGameUserQuestCharacterHeartPartySaveDataRecord] = None
class QuestOutGameApiGetUserQuestMissionDataListResponse(ResponseBase):
    userQuestMissionDataList: List[QuestOutGameUserQuestMissionDataRecord] = None
class ConfigApiGetConfigResponse(ResponseBase):
    loginBonusConfig: LoginBonusLoginBonusConfig = None
    characterConfig: CharacterCharacterConfig = None
    cardConfig: CardCardConfig = None
    collectionConfig: CollectionCollectionConfig = None
    styleConfig: StyleStyleConfig = None
    pvpConfig: PvpPvpConfig = None
    talismanConfig: TalismanTalismanConfig = None
    missionConfig: MissionMissionConfig = None
    guildConfig: GuildGuildConfig = None
    gveConfig: GveGveConfig = None
    presentBoxConfig: PresentPresentBoxConfig = None
    userConfig: UserUserConfig = None
    questConfig: QuestOutGameQuestConfig = None
    tutorialConfig: TutorialTutorialConfig = None
    towerConfig: TowerTowerConfig = None
    partyConfig: PartyPartyConfig = None
    subscriptionConfig: ShopSubscriptionConfig = None
    storyEventConfig: StoryEventStoryEventConfig = None
    chatConfig: ChatChatConfig = None
    firestoreConfig: ConfigFirestoreConfig = None
    termsConfig: TermsTermsConfig = None
    gatheringConfig: GatheringGatheringConfig = None
    gvgConfig: GvgGvgConfig = None
    scoreAttackConfig: ScoreAttackScoreAttackConfig = None
    appResourceConfig: ConfigAppResourceConfig = None
    isPreRelease: bool = None
    purgeConfig: ConfigPurgeConfig = None
    selectionAbilityConfig: SelectionAbilitySelectionAbilityConfig = None
    multiRaidConfig: MultiRaidMultiRaidConfig = None
class CollectionApiGetCollectionDataListResponse(ResponseBase):
    collectionDataList: List[CollectionCollectionDataRecord] = None
    collectionIllustAchieveDataList: List[CollectionCollectionIllustAchieveDataRecord] = None
    fieldStageCollectionInfoList: List[CollectionFieldStageCollectionInfo] = None
    isMagiaRecordLinkedUser: bool = None
class CollectionApiGetCollectionParamUpAchieveDataListResponse(ResponseBase):
    collectionParamUpAchieveDataList: List[CollectionCollectionParamUpAchieveDataRecord] = None
    isMagiaRecordLinkedUser: bool = None
class CollectionApiUpdateAlreadyViewResponse(ResponseBase):
    collectionDataList: List[CollectionCollectionDataRecord] = None
    cardDataList: List[CardCardDataRecord] = None
class CollectionApiEndCompleteProgressResponse(ResponseBase):
    collectionParamUpAchieveData: CollectionCollectionParamUpAchieveDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
    objectDataRecord: ObjectObjectDataRecord = None
class CollectionApiGetMagiaRecordCollectionInfoResponse(ResponseBase):
    magiaRecordCharacterMstList: List[CollectionMagiaRecordCharacterMstRecord] = None
    magiaRecordMemoriaMstList: List[CollectionMagiaRecordMemoriaMstRecord] = None
class CollectionApiAdvReadResponse(ResponseBase):
    isSuccess: bool = None
class CollectionApiGetCollectionIllustAchieveDataResponse(ResponseBase):
    collectionIllustAchieveData: CollectionCollectionIllustAchieveDataRecord = None
class CollectionApiViewNewCollectionIllustEffectResponse(ResponseBase):
    collectionIllustAchieveData: CollectionCollectionIllustAchieveDataRecord = None
class ChatApiCreateGroupChatRoomResponse(ResponseBase):
    chatRoomInfo: ChatChatRoomInfo = None
    uninvitedUserIdList: List[int] = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ChatApiAddUserToGroupChatRoomResponse(ResponseBase):
    uninvitedUserIdList: List[int] = None
class ChatApiDeleteUserByGroupChatRoomResponse(ResponseBase):
    isSuccess: bool = None
class ChatApiLeaveGroupChatRoomResponse(ResponseBase):
    isSuccess: bool = None
class ChatApiCreateDirectChatRoomResponse(ResponseBase):
    chatRoomInfo: ChatChatRoomInfo = None
    deleteRoomDocumentId: str = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ChatApiLeaveDirectChatRoomResponse(ResponseBase):
    isSuccess: bool = None
class ChatApiApproveEnterChatRoomResponse(ResponseBase):
    isSuccess: bool = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ChatApiDeleteOwnChatMessageResponse(ResponseBase):
    isSuccess: bool = None
class ChatApiGetChatBlockUserListResponse(ResponseBase):
    userDisplayInfoList: List[UserUserDisplayInfo] = None
class ChatApiBlockChatUserResponse(ResponseBase):
    isSuccess: bool = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ChatApiUnblockChatUserResponse(ResponseBase):
    isSuccess: bool = None
class ChatApiSearchChatUserResponse(ResponseBase):
    userDisplayInfoList: List[UserUserDisplayInfo] = None
class PartyApiGetPartyDataListResponse(ResponseBase):
    partyDataList: List[PartyPartyDataRecord] = None
class PartyApiGetCharacterBuildDataListResponse(ResponseBase):
    characterBuildDataList: List[PartyCharacterBuildDataRecord] = None
class PartyApiSavePartyResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
    characterBuildDataList: List[PartyCharacterBuildDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class PartyApiSavePartyLeaderResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
class PartyApiSavePartyNameResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
class PartyApiSavePartyRoleResponse(ResponseBase):
    partyDataList: List[PartyPartyDataRecord] = None
class PartyApiSavePartyForRecommendResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
    userParamData: UserUserParamDataRecord = None
class PartyApiGetRecommendPartyDataResponse(ResponseBase):
    recommendPartyData: PartyPartyDataRecord = None
class PartyApiGetRecommendSubStyleResponse(ResponseBase):
    recommendSubStyleMstIdList: List[int] = None
class PartyApiGetRecommendCardResponse(ResponseBase):
    recommendCardDataIdList: List[int] = None
    recommendSubCardDataIdList: List[int] = None
class PartyApiRemovePartyResponse(ResponseBase):
    partyDataId: int = None
class PartyApiSavePartyCardResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
    userParamData: UserUserParamDataRecord = None
class PartyApiSavePartySubStyleResponse(ResponseBase):
    partyData: PartyPartyDataRecord = None
    userParamData: UserUserParamDataRecord = None
class CharacterApiGetCharacterListResponse(ResponseBase):
    characterDataList: List[CharacterCharacterDataRecord] = None
class CharacterApiCharacterAwakeResponse(ResponseBase):
    characterData: CharacterCharacterDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
class CharacterApiCharacterLevelUpResponse(ResponseBase):
    characterData: CharacterCharacterDataRecord = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    itemDataList: List[ItemItemDataRecord] = None
    partyDataList: List[PartyPartyDataRecord] = None
class CharacterApiCharacterHeartLevelUpResponse(ResponseBase):
    objectDataRecord: ObjectObjectDataRecord = None
    characterHeartLevelUpInfo: CharacterCharacterHeartLevelUpInfo = None
    partyDataList: List[PartyPartyDataRecord] = None
class CardApiGetCardListResponse(ResponseBase):
    cardDataList: List[CardCardDataRecord] = None
class CardApiCardLimitBreakResponse(ResponseBase):
    cardData: CardCardDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    deletedCardDataIds: List[int] = None
class CardApiCardSellResponse(ResponseBase):
    deletedCardDataIds: List[int] = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
class CardApiSetCardProtectResponse(ResponseBase):
    cardData: CardCardDataRecord = None
class CardApiUpdateAlreadyViewResponse(ResponseBase):
    cardDataList: List[CardCardDataRecord] = None
class CardApiCardPassiveSkillLevelUpResponse(ResponseBase):
    cardData: CardCardDataRecord = None
    itemDataList: List[ItemItemDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
class QuestBattleApiInitializeStageResponse(ResponseBase):
    initializeStatus: int = None
    questRoomData: QuestBattleQuestRoomData = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    partyDataList: List[PartyPartyDataRecord] = None
    isNotUseStaminaFirstClear: bool = None
class QuestBattleApiGetQuestInfoResponse(ResponseBase):
    stageInfo: QuestBattleStageInfo = None
    allyBattleUnitList: List[QuestBattleBattleUnit] = None
    allyCharacterBuildDetailList: List[PartyCharacterBuildDetail] = None
    repeatNum: int = None
class QuestBattleApiFinalizeStageForUserResponse(ResponseBase):
    result: QuestBattleResult = None
    beforeLevel: int = None
    afterLevel: int = None
    beforeExp: int = None
    afterExp: int = None
    beforeStamina: int = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    acquiredQuestBonusRewardInfoList: List[QuestBattleAcquiredQuestBonusRewardInfo] = None
    canReplay: bool = None
    remainPlayCount: int = None
    objectDataRecord: ObjectObjectDataRecord = None
    keyItemDataList: List[ItemItemDataRecord] = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    styleLevelUpInfoList: List[StyleStyleLevelUpInfo] = None
    partyDataList: List[PartyPartyDataRecord] = None
    eventItemObjectReceiveType: int = None
    eventItemId: int = None
    baseEventItemNum: int = None
    addBonusEventItemNum: int = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
    userQuestTrainingData: QuestOutGameUserQuestTrainingDataRecord = None
    storyEventData: StoryEventStoryEventDataRecord = None
    characterHeartLevelUpInfoList: List[CharacterCharacterHeartLevelUpInfo] = None
    userQuestCharacterHeartData: QuestOutGameUserQuestCharacterHeartDataRecord = None
    userQuestCharacterHeartPartySaveData: QuestOutGameUserQuestCharacterHeartPartySaveDataRecord = None
    canQuestCharacterHeartNextStage: bool = None
    userTowerData: TowerUserTowerDataRecord = None
    acquiredRewardMoney: int = None
    isSkipTrainingQuestNotClearUnderNowRank: bool = None
    selectionAbilityDataList: List[SelectionAbilitySelectionAbilityDataRecord] = None
    acquiredSelectionAbilityInfoList: List[SelectionAbilityAcquiredSelectionAbilityInfo] = None
    selectionAbilityConversionItemDataList: List[SelectionAbilitySelectionAbilityConversionItemData] = None
    isUserExpStoredMessage: bool = None
class QuestBattleApiRetireResponse(ResponseBase):
    isSuccess: bool = None
    userParamData: UserUserParamDataRecord = None
class QuestBattleApiSkipQuestBattleResponse(ResponseBase):
    result: QuestBattleResult = None
    beforeLevel: int = None
    afterLevel: int = None
    beforeExp: int = None
    afterExp: int = None
    beforeStamina: int = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    acquiredQuestBonusRewardInfoList: List[QuestBattleAcquiredQuestBonusRewardInfo] = None
    canReplay: bool = None
    remainPlayCount: int = None
    objectDataRecord: ObjectObjectDataRecord = None
    keyItemDataList: List[ItemItemDataRecord] = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    styleLevelUpInfoList: List[StyleStyleLevelUpInfo] = None
    partyDataList: List[PartyPartyDataRecord] = None
    eventItemObjectReceiveType: int = None
    eventItemId: int = None
    baseEventItemNum: int = None
    addBonusEventItemNum: int = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
    userQuestTrainingData: QuestOutGameUserQuestTrainingDataRecord = None
    storyEventData: StoryEventStoryEventDataRecord = None
    characterHeartLevelUpInfoList: List[CharacterCharacterHeartLevelUpInfo] = None
    userQuestCharacterHeartData: QuestOutGameUserQuestCharacterHeartDataRecord = None
    userQuestCharacterHeartPartySaveData: QuestOutGameUserQuestCharacterHeartPartySaveDataRecord = None
    acquiredRewardMoney: int = None
    isUserExpStoredMessage: bool = None
class QuestBattleApiGetBackGroundInfoResponse(ResponseBase):
    questRoomData: QuestBattleQuestRoomData = None
    userQuestStageData: QuestOutGameUserQuestStageDataRecord = None
class ExplorationApiGetTopInfoV4Response(ResponseBase):
    isFirstEntry: bool = None
    totalPowerSkipRate: int = None
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
    collectionDataList: List[CollectionCollectionDataRecord] = None
    forceFirstEntryFieldPointMstId: int = None
class ExplorationApiReachFieldPointResponse(ResponseBase):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
class ExplorationApiOccurDungeonEventResponse(ResponseBase):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
class ExplorationApiDungeonStartResponse(ResponseBase):
    isSuccess: bool = None
class ExplorationApiDungeonGoalResponse(ResponseBase):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
    objectDataRecord: ObjectObjectDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    achievedConditionGroupIds: List[int] = None
    fieldStageCollectionInfo: CollectionFieldStageCollectionInfo = None
    partyDataList: List[PartyPartyDataRecord] = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ExplorationApiSkipFieldPointResponse(ResponseBase):
    dungeonResult: ExplorationDungeonResult = None
    battleResult: ExplorationBattleExplorationBattleResult = None
    objectDataRecordByDungeon: ObjectObjectDataRecord = None
    partyDataListByDungeon: List[PartyPartyDataRecord] = None
    miniTutorialDataByDungeon: TutorialMiniTutorialDataRecord = None
    objectDataRecordByBattle: ObjectObjectDataRecord = None
    partyDataListByBattle: List[PartyPartyDataRecord] = None
    miniTutorialDataByBattle: TutorialMiniTutorialDataRecord = None
class ExplorationApiClearFieldPointStoryResponse(ResponseBase):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
    achievedConditionGroupIds: List[int] = None
    collectionDataList: List[CollectionCollectionDataRecord] = None
    miniTutorialData: TutorialMiniTutorialDataRecord = None
class ExplorationApiResetDungeonProgressResponse(ResponseBase):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
class ExplorationApiGetEnableStageListResponse(ResponseBase):
    fieldStageMstIdList: List[int] = None
class ExplorationApiGetStageMstListResponse(ResponseBase):
    fieldStratumMstList: List[ExplorationFieldStratumMstRecord] = None
    fieldPointMstList: List[ExplorationFieldPointMstRecord] = None
    dungeonMstList: List[DungeonDungeonMstRecord] = None
    dungeonRoomMstList: List[DungeonDungeonRoomMstRecord] = None
    dungeonEventMstList: List[DungeonDungeonEventMstRecord] = None
    collectionConditionGroupMstList: List[CollectionCollectionConditionGroupMstRecord] = None
    collectionConditionMstList: List[CollectionCollectionConditionMstRecord] = None
    collectionDataList: List[CollectionCollectionDataRecord] = None
class ExplorationApiGetDungeonMstListResponse(ResponseBase):
    dungeonTypeMst: DungeonDungeonTypeMstRecord = None
    dungeonRoomMstList: List[DungeonDungeonRoomMstRecord] = None
    dungeonEventMstList: List[DungeonDungeonEventMstRecord] = None
class ExplorationApiGetFieldStageCollectionInfoListResponse(ResponseBase):
    questMapEffectedInfoList: List[ExplorationQuestMapEffectedInfo] = None
    fieldStageCollectionInfoList: List[CollectionFieldStageCollectionInfo] = None
    collectionIllustAchieveDataList: List[CollectionCollectionIllustAchieveDataRecord] = None
class ExplorationApiUpdateUserQuestMapEffectedDataResponse(ResponseBase):
    result: bool = None
