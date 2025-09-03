from typing import List, Dict
from .enums import *
from pydantic import BaseModel, Field

class WebPayPurchaseResultRecord(BaseModel):
    purchaseId: str = None
    status: int = None
class TitleTitleViewData(BaseModel):
    isMaintenance: bool = None
    isDbMaintenance: bool = None
    maintenanceMessage: str = None
    dbMaintenanceForAnnounceText: str = None
class TermsTermsInfo(BaseModel):
    termsNum: int = None
    text: str = None
class UserUserDataRecord(BaseModel):
    userId: int = None
    uuid: str = None
    playerId: str = None
    banType: int = None
    osType: int = None
    storeType: int = None
    language: str = None
    region: str = None
    timezone: str = None
    termsNumIos: int = None
    termsNumAndroid: int = None
    termsNumWindows: int = None
    termsNumBrowser: int = None
    termsNumChat: int = None
class TalismanTalismanDataRecord(BaseModel):
    userId: int = None
    talismanDataId: int = None
    talismanMstId: int = None
    level: int = None
    mainParamMstId: int = None
    sub1ParamMstId: int = None
    sub2ParamMstId: int = None
    sub3ParamMstId: int = None
    sub4ParamMstId: int = None
    createdTime: str = None
    isProtect: bool = None
class UserUserParamDataRecord(BaseModel):
    userId: int = None
    name: str = None
    nameUpdatedTime: str = None
    missionClearCount: int = None
    money: int = None
    totalMoney: int = None
    level: int = None
    exp: int = None
    totalExp: int = None
    stamina: int = None
    staminaUpdatedTime: str = None
    recoveryCount: int = None
    recoveryResetTime: str = None
    gemRecoveryCount: int = None
    gemRecoveryResetTime: str = None
    pvpWin: int = None
    pvpLose: int = None
    pvpWinRate: float = None
    favoriteStyleMstId: int = None
    tutorialStep: int = None
    tutorialFinishTime: str = None
    recentLoginTime: str = None
    recentStoreReviewTime: str = None
    setUserTitleMstIds: str = None
    maxPartyPower: int = None
    clearedFieldStageMstId: int = None
    accountStatus: int = None
class PartyPartyDataRecord(BaseModel):
    userId: int = None
    partyDataId: int = None
    name: str = None
    partyType: int = None
    isQuest: bool = None
    isPvp: bool = None
    isExploration: bool = None
    isMapGve: bool = None
    isScoreAttack: bool = None
    isMultiRaid: bool = None
    member1: int = None
    cardMstId1: int = None
    subStyleMstIds1: str = None
    member2: int = None
    cardMstId2: int = None
    subStyleMstIds2: str = None
    member3: int = None
    cardMstId3: int = None
    subStyleMstIds3: str = None
    member4: int = None
    cardMstId4: int = None
    subStyleMstIds4: str = None
    member5: int = None
    cardMstId5: int = None
    subStyleMstIds5: str = None
    leaderStyleMstId: int = None
    partyPower: int = None
    partyIndex: int = None
class ItemItemMstRecord(BaseModel):
    itemMstId: int = None
    name: str = None
    description: str = None
    type: int = None
    detailType: int = None
    effectType: int = None
    effectValue: int = None
    effectValue2: int = None
    rarity: int = None
    canSell: bool = None
    price: int = None
    canUse: bool = None
    sortOrder: int = None
    maxNum: int = None
    validDays: int = None
    startTime: str = None
    endTime: str = None
    transitionSceneName: str = None
    resourceName: str = None
    isConversion: bool = None
class CardCardMstRecord(BaseModel):
    cardMstId: int = None
    name: str = None
    illustrator: str = None
    source: str = None
    rarity: int = None
    element: int = None
    passiveSkill1: int = None
    passiveSkill2: int = None
    passiveSkill3: int = None
    resourceName: str = None
    characterMstId: int = None
    unlockTypeCsv: str = None
    unlockIdCsv: str = None
    advPosition: int = None
    releaseTime: str = None
class CardCardLimitBreakMstRecord(BaseModel):
    cardLimitBreakMstId: int = None
    cardMstId: int = None
    limitBreakCount: int = None
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
class SkillSkillMstRecord(BaseModel):
    skillMstId: int = None
    skillUniqueId: int = None
    level: int = None
    name: str = None
    description: str = None
    type: int = None
    sp: int = None
    hitEffectResourceName: str = None
    balloonText: str = None
    iconName: str = None
    directionName: str = None
    cueSheetName: str = None
    cueName: str = None
    isEmphasize: bool = None
    additionalCueName: str = None
    skillButtonIcon: str = None
class SkillSkillLevelUpConditionMstRecord(BaseModel):
    skillLevelUpConditionMstId: int = None
    skillLevelUpType: int = None
    rarity: int = None
    minLevel: int = None
    conditionType: int = None
    conditionValue: int = None
    useMoney: int = None
    itemMstId1: int = None
    itemNum1: int = None
    itemMstId2: int = None
    itemNum2: int = None
    itemMstId3: int = None
    itemNum3: int = None
class CharacterCharacterAwakeMstRecord(BaseModel):
    characterAwakeMstId: int = None
    awakeLevel: int = None
    addHp: int = None
    addAtk: int = None
    addDef: int = None
    rateHp: int = None
    rateAtk: int = None
    rateDef: int = None
class CharacterCharacterMstRecord(BaseModel):
    characterMstId: int = None
    name: str = None
    awakeItemMstId: int = None
    iconResourceName: str = None
    colorCode: str = None
class CharacterCharacterProfileMstRecord(BaseModel):
    characterMstId: int = None
    description: str = None
    characterVoice: str = None
    schoolName: str = None
    age: str = None
    weapon: str = None
    gift: str = None
    weakPoint: str = None
    seriesId: int = None
    regionId: int = None
    teamId1: int = None
    teamId2: int = None
    sortOrder: int = None
class CharacterCharacterHeartMstRecord(BaseModel):
    characterHeartMstId: int = None
    characterMstId: int = None
    paramUpGroupId: int = None
    objectRewardGroupId: int = None
class CharacterCharacterHeartParamUpGroupMstRecord(BaseModel):
    characterHeartParamUpGroupMstId: int = None
    paramUpGroupId: int = None
    heartLevel: int = None
    styleParamUpEffectMstId: int = None
class CharacterCharacterHeartObjectRewardMstRecord(BaseModel):
    characterHeartObjectRewardMstId: int = None
    objectRewardGroupId: int = None
    heartLevel: int = None
    objectReceiveType: int = None
    objectId: int = None
class CharacterCharacterHeartLevelUpMstRecord(BaseModel):
    characterHeartLevelUpMstId: int = None
    heartLevel: int = None
    heartLevelUpExp: int = None
class CharacterCharacterTeamMstRecord(BaseModel):
    characterTeamMstId: int = None
    name: str = None
    sortOrder: int = None
class CharacterReplaceCharacterNameMstRecord(BaseModel):
    replaceCharacterNameMstId: int = None
    styleMstId: int = None
    overrideCharacterName: str = None
class StyleStyleMstRecord(BaseModel):
    styleMstId: int = None
    name: str = None
    styleFigureMstId: int = None
    rarity: int = None
    specialAttackMstId: int = None
    normalAttack: int = None
    skill1: int = None
    passiveSkill1: int = None
    limitBreakPassiveSkill1: int = None
    subPassiveSkill: int = None
    leaderSkill: int = None
    hp: int = None
    ep: int = None
    recoveryEpRate: int = None
    atk: int = None
    _def: int = Field(alias='def')
    speed: int = None
    criticalRate: int = None
    criticalDamageRate: int = None
    breakDamageRate: int = None
    healRate: int = None
    effectHitRate: int = None
    effectParryRate: int = None
    fireDamageRate: int = None
    aquaDamageRate: int = None
    forestDamageRate: int = None
    lightDamageRate: int = None
    darkDamageRate: int = None
    neutralDamageRate: int = None
    fireResistRate: int = None
    aquaResistRate: int = None
    forestResistRate: int = None
    lightResistRate: int = None
    darkResistRate: int = None
    neutralResistRate: int = None
    element: int = None
    role: int = None
    paramUpGroupId: int = None
    resourceName: str = None
    releaseTime: str = None
    isCollectionDisp: bool = None
class TowerTowerMstRecord(BaseModel):
    towerMstId: int = None
    eventType: int = None
    startTime: str = None
    endTime: str = None
    reprintNum: int = None
class QuestOutGameQuestCategoryMstRecord(BaseModel):
    questCategoryMstId: int = None
    name: str = None
    resourceName: str = None
class QuestOutGameQuestMapMstRecord(BaseModel):
    questMapMstId: int = None
    questCategoryMstId: int = None
    name: str = None
    conditionGroupId: int = None
    openFlagMiniTutorialNumber: int = None
    openEffectFlagMiniTutorialNumber: int = None
class QuestOutGameQuestGroupMstRecord(BaseModel):
    questGroupMstId: int = None
    questCategoryMstId: int = None
    questMapMstId: int = None
    groupType: int = None
    name: str = None
    resourceName: str = None
    startTime: str = None
    endTime: str = None
    sortOrder: int = None
    priorityTerm: int = None
    dailyBattleClearLimit: int = None
    playableWeekDays: str = None
    keyQuestType: int = None
    keyItemMstId: int = None
    reprintNum: int = None
class QuestOutGameQuestStageMstRecord(BaseModel):
    questStageMstId: int = None
    questGroupMstId: int = None
    name: str = None
    description: str = None
    detail: str = None
    difficulty: int = None
    useStamina: int = None
    prevQuestStageMstId: int = None
    conditionGroupId: int = None
    questMissionGroupId: int = None
    resourceName: str = None
    recommendationElementCsv: str = None
    recommendationPartyPower: int = None
    rewardGroupId: int = None
    firstClearRewardGroupId: int = None
    exp: int = None
    firstClearExp: int = None
    money: int = None
    firstClearMoney: int = None
    characterExp: int = None
    styleExp: int = None
    firstClearStyleExp: int = None
    characterHeartExp: int = None
    bgmCueSheetName: str = None
    bgmCueName: str = None
    stagePrefabName: str = None
    judgeResultType: int = None
    judgeResultValue: int = None
    beforeBattleScenarioMstId: int = None
    afterBattleScenarioMstId: int = None
    endDirectionName: str = None
    overrideComponentPrefabName: str = None
    isAutoModeOff: int = None
    selectionAbilityLotteryMstId: int = None
    element: int = None
    recommendationElement: int = None
class QuestOutGameQuestConditionMstRecord(BaseModel):
    questConditionMstId: int = None
    conditionGroupId: int = None
    conditionType: int = None
    value1: int = None
    value2: int = None
class MissionMissionTitleMstRecord(BaseModel):
    missionTitleMstId: int = None
    prevMissionTitleMstId: int = None
    title: str = None
    priority: int = None
    featuredRewardResourceName: str = None
class MissionMissionTransitionMstRecord(BaseModel):
    missionTransitionMstId: int = None
    missionMstId: int = None
    transitionSceneName: str = None
    transitionSceneParam: int = None
class MissionSubscriptionMissionRewardMstRecord(BaseModel):
    missionMstId: int = None
    subscriptionLabel: str = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class MissionMissionMstRecord(BaseModel):
    missionMstId: int = None
    missionTitleMstId: int = None
    sortOrder: int = None
    missionType: int = None
    category: int = None
    missionUniqueId: int = None
    missionUniquePriority: int = None
    isOverCount: bool = None
    title: str = None
    description: str = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    resetType: int = None
    resetCycle: int = None
    triggerType: int = None
    conditionType: int = None
    conditionObjectId: int = None
    conditionObjectId2: int = None
    conditionObjectId2OperatorType: int = None
    conditionCount: int = None
    startTime: str = None
    endTime: str = None
class QuestOutGameEnemyMstRecord(BaseModel):
    enemyMstId: int = None
    enemyUniqueId: int = None
    name: str = None
    runesName: str = None
    enemyType: int = None
    size: int = None
    modelPrefabName: str = None
    iconResourceName: str = None
    cueSheetName: str = None
    appearEffectPrefabName: str = None
    isCollectionDisp: bool = None
    canRotateModel: bool = None
    unlockType: int = None
    releaseTime: str = None
    isNoVisualDeath: bool = None
class QuestOutGameEnemyProfileMstRecord(BaseModel):
    enemyProfileMstId: int = None
    enemyUniqueId: int = None
    enemyMstId: int = None
    name: str = None
    runesName: str = None
    seriesId: int = None
    description: str = None
    sortOrder: int = None
    isCollectionDisp: bool = None
    unlockType: int = None
    unlockId: int = None
    releaseTime: str = None
class QuestOutGameQuestEnemyAppearanceMstRecord(BaseModel):
    questEnemyAppearanceMstId: int = None
    questStageMstId: int = None
    wave: int = None
    enemyMstId: int = None
    enemySkillSetId: int = None
    enemyConditionSkillSetId: int = None
    passiveSkillMstId: int = None
    weakElement1: int = None
    weakElement2: int = None
    weakElement3: int = None
    weakElement4: int = None
    weakElement5: int = None
    weakElement6: int = None
    isMainTargetEnemy: bool = None
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
    speed: int = None
    criticalRate: int = None
    criticalDamageRate: int = None
    healRate: int = None
    effectHitRate: int = None
    effectParryRate: int = None
    burnParryRate: int = None
    weaknessParryRate: int = None
    poisonParryRate: int = None
    stunParryRate: int = None
    curseParryRate: int = None
    bleedParryRate: int = None
    vortexParryRate: int = None
    fireDamageRate: int = None
    aquaDamageRate: int = None
    forestDamageRate: int = None
    lightDamageRate: int = None
    darkDamageRate: int = None
    neutralDamageRate: int = None
    fireResistRate: int = None
    aquaResistRate: int = None
    forestResistRate: int = None
    lightResistRate: int = None
    darkResistRate: int = None
    neutralResistRate: int = None
    fireAimDamageRate: int = None
    aquaAimDamageRate: int = None
    forestAimDamageRate: int = None
    lightAimDamageRate: int = None
    darkAimDamageRate: int = None
    neutralAimDamageRate: int = None
    breakMstId: int = None
    conditionType: int = None
    conditionValue: int = None
    summonId: int = None
    hpGaugeCount: int = None
    startHpGaugeCount: int = None
    modeChangeEffectTxt: str = None
class QuestOutGameQuestEnemySkillSetMstRecord(BaseModel):
    questEnemySkillSetMstId: int = None
    enemySkillSetId: int = None
    skillMstId: int = None
    weightValue: int = None
    hpGaugeValue: int = None
    isDescriptionHidden: bool = None
class QuestOutGameBreakMstRecord(BaseModel):
    breakMstId: int = None
    breakPoint: int = None
    breakPointRecoveryPerTurn: int = None
    breakTurnGaugeSlowRatio: int = None
    initialBreakedDamageReceiveRate: int = None
    maxBreakedDamageReceiveRate: int = None
    breakedDamageReceiveRateIncreaseRate: int = None
class SkillAbilityEffectTypeMstRecord(BaseModel):
    abilityEffectTypeMstId: int = None
    name: str = None
    effectType: str = None
    category: int = None
    targetParams: str = None
    paramEffectType: int = None
    iconName: str = None
    stateFlipName: str = None
    displayType: int = None
class SkillSkillDetailMstRecord(BaseModel):
    skillDetailMstId: int = None
    skillMstId: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
    value3: int = None
    value4: int = None
    value5: int = None
    element: int = None
    turn: int = None
    remainCount: int = None
    role: int = None
    range: int = None
    probability: int = None
    description: str = None
    descriptionType: int = None
    startConditionSetIdCsv: str = None
    activeConditionSetIdCsv: str = None
class QuestOutGameQuestRewardMstRecord(BaseModel):
    questRewardMstId: int = None
    rewardGroupId: int = None
    sortOrder: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ExplorationFieldSeriesMstRecord(BaseModel):
    fieldSeriesMstId: int = None
    name: str = None
    questMapMstId: int = None
    questGroupMstId: int = None
    styleMstId: int = None
    assetbundleName: str = None
    startTime: str = None
    endTime: str = None
    sortOrder: int = None
    advMstId: int = None
class ExplorationFieldStageMstRecord(BaseModel):
    fieldStageMstId: int = None
    fieldSeriesMstId: int = None
    name: str = None
    subTitle: str = None
    difficulty: int = None
    prevFieldStageMstId: int = None
    prevFieldStageMstId2: int = None
    firstClearRewardGroupId: int = None
    stageAssetbundleName: str = None
    backgroundCardMstId: int = None
class ExplorationAdvMstRecord(BaseModel):
    advMstId: int = None
    advType: int = None
    has3dMovie: bool = None
    advTitleMstId: int = None
    name: str = None
    subName: str = None
    advAssetbundleName: str = None
    advResourceName: str = None
    unlockType: int = None
    unlockId: int = None
    gainGemFlg: bool = None
    beforeAdvMstIdInGallery: int = None
    releaseTime: str = None
class ExplorationAdvTitleMstRecord(BaseModel):
    advTitleMstId: int = None
    title: str = None
    isViewCollection: bool = None
class ObjectObjectReceiveTypeMstRecord(BaseModel):
    objectReceiveType: int = None
    objectType: int = None
    expireDate: int = None
class ObjectPayTypeMstRecord(BaseModel):
    payType: int = None
    objectType: int = None
class TalismanTalismanMstRecord(BaseModel):
    talismanMstId: int = None
    name: str = None
    rarity: int = None
    talismanSlotId: int = None
    talismanSeriesMstId: int = None
    resourceName: str = None
class TalismanTalismanParamMstRecord(BaseModel):
    talismanParamMstId: int = None
    talismanParamEffectMstId: int = None
    level: int = None
    rarity: int = None
    talismanSlotId: int = None
    talismanParamType: int = None
    value: int = None
    description: str = None
class TalismanTalismanParamEffectMstRecord(BaseModel):
    talismanParamEffectMstId: int = None
    abilityEffectType: str = None
    element: int = None
    stance: int = None
    description: str = None
class TalismanTalismanSeriesMstRecord(BaseModel):
    talismanSeriesMstId: int = None
    talismanSeriesName: str = None
    slot2PassiveSkillMstId: int = None
    slot4PassiveSkillMstId: int = None
    resourceName: str = None
class SkillPassiveSkillMstRecord(BaseModel):
    passiveSkillMstId: int = None
    skillUniqueId: int = None
    level: int = None
    name: str = None
    description: str = None
    conditionElement: int = None
    conditionRole: int = None
    skillButtonIcon: str = None
class SkillPassiveSkillDetailMstRecord(BaseModel):
    passiveSkillDetailMstId: int = None
    passiveSkillMstId: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
    value3: int = None
    element: int = None
    turn: int = None
    remainCount: int = None
    role: int = None
    range: int = None
    description: str = None
    descriptionType: int = None
    startTimingIdCsv: str = None
    startConditionSetIdCsv: str = None
    activeConditionSetIdCsv: str = None
class SkillLeaderSkillMstRecord(BaseModel):
    leaderSkillMstId: int = None
    name: str = None
    description: str = None
class SkillLeaderSkillDetailMstRecord(BaseModel):
    leaderSkillDetailMstId: int = None
    leaderSkillMstId: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
    value3: int = None
    element: int = None
    stance: int = None
    description: str = None
class PvpPvpRankingRewardMstRecord(BaseModel):
    pvpRankingRewardMstId: int = None
    ranking: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class PvpPvpPointRewardMstRecord(BaseModel):
    pvpPointRewardMstId: int = None
    point: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class UserTitleUserTitleMstRecord(BaseModel):
    userTitleMstId: int = None
    title: str = None
    titleType: int = None
    value1: int = None
class GuildGuildTitleMstRecord(BaseModel):
    guildTitleMstId: int = None
    title: str = None
    hasDefault: bool = None
    description: str = None
    resourceName: str = None
class UserUserLevelUpMstRecord(BaseModel):
    level: int = None
    levelUpExp: int = None
    backGroundPlayLimitSeconds: int = None
    subStyleSlotNum: int = None
    maxStamina: int = None
    startTime: str = None
class ShopShopSeriesMstRecord(BaseModel):
    shopSeriesMstId: int = None
    title: str = None
    description: str = None
    category: int = None
    startTime: str = None
    endTime: str = None
    shopGroupId1: int = None
    shopGroupId2: int = None
    payType: int = None
    payId: int = None
    resourceName: str = None
class ShopShopMstRecord(BaseModel):
    shopMstId: int = None
    shopGroupId: int = None
    name: str = None
    description: str = None
    sortOrder: int = None
    payType: int = None
    payId: int = None
    price: int = None
    purchaseLimitCount: int = None
    resetType: int = None
    isSale: bool = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    detailGroupId: int = None
    resourceName: str = None
    startTime: str = None
    endTime: str = None
class ShopShopDetailMstRecord(BaseModel):
    shopDetailMstId: int = None
    detailGroupId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class HomeBannerMstRecord(BaseModel):
    bannerMstId: int = None
    name: str = None
    imageName: str = None
    destination: str = None
    bannerLabelMstId: int = None
class HomeBannerLabelMstRecord(BaseModel):
    bannerLabelMstId: int = None
    labelContent: str = None
    labelBgColor: str = None
class HomeHomeBannerMstRecord(BaseModel):
    homeBannerMstId: int = None
    bannerMstId: int = None
    startTime: str = None
    endTime: str = None
    sortOrder: int = None
    osType: int = None
class HomeHomeAppealMstRecord(BaseModel):
    homeAppealMstId: int = None
    type: int = None
    bannerType: int = None
    resourceName: str = None
    bannerText1: str = None
    bannerText2: str = None
    bannerText3: str = None
    bannerText4: str = None
    textColor: str = None
    partsColor: str = None
    styleMstId1: int = None
    styleMstId2: int = None
    styleMstId3: int = None
    styleFigureMstId1: int = None
    styleFigureMstId2: int = None
    styleFigureMstId3: int = None
    transitionSceneName: str = None
    transitionSceneParam: str = None
    startTime: str = None
    endTime: str = None
    targetRegionType: int = None
    sortOrder: int = None
class TipsTipsMstRecord(BaseModel):
    tipsMstId: int = None
    title: str = None
    description: str = None
    imageResourceName: str = None
    level: int = None
class GveGveMstRecord(BaseModel):
    gveMstId: int = None
    startTime: str = None
    endTime: str = None
    battleStartTime: str = None
    battleEndTime: str = None
    gainEpUpRate: int = None
    specialAttackDamageUpRate: int = None
    resourceName: str = None
class GveGveStageMstRecord(BaseModel):
    gveStageMstId: int = None
    gveMstId: int = None
    laps: int = None
    step: int = None
    questStageMstId: int = None
    breakBonusTriggerCount: int = None
    characteristic: str = None
    victoryRound: int = None
class GveGveStageRewardMstRecord(BaseModel):
    gveStageRewardMstId: int = None
    gveStageMstId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class MapGveMapGveMstRecord(BaseModel):
    mapGveMstId: int = None
    startTime: str = None
    endTime: str = None
    battleStartTime: str = None
    battleEndTime: str = None
    gainEpUpRate: int = None
    specialAttackDamageUpRate: int = None
    stageAssetbundleName: str = None
class MapGveMapGveAreaMstRecord(BaseModel):
    mapGveAreaMstId: int = None
    mapGveMstId: int = None
    areaNum: int = None
class MapGveMapGvePointMstRecord(BaseModel):
    mapGvePointMstId: int = None
    mapGveAreaMstId: int = None
    prevMapGvePointMstId: int = None
    pointType: int = None
    pointValue1: int = None
    pointValue2: int = None
    pointValue3: int = None
    isLock: bool = None
    coordinateId: int = None
class LoginBonusLoginBonusMstRecord(BaseModel):
    loginBonusMstId: int = None
    title: str = None
    cycleType: int = None
    sortOrder: int = None
    startTime: str = None
    endTime: str = None
class LoginBonusLoginBonusRewardMstRecord(BaseModel):
    loginBonusRewardMstId: int = None
    loginBonusMstId: int = None
    dayCount: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class StyleStyleFigureMstRecord(BaseModel):
    styleFigureMstId: int = None
    characterMstId: int = None
    modelName: str = None
    iconName: str = None
    voiceCueSheetName: str = None
    sortOrder: int = None
class StyleStyleFigureStoryMstRecord(BaseModel):
    styleFigureStoryMstId: int = None
    styleFigureMstId: int = None
    advMstId: int = None
class StyleStyleParamUpTreeMstRecord(BaseModel):
    styleParamUpTreeMstId: int = None
    styleMstId: int = None
    treeName: str = None
    priority: int = None
    useItemMstId1: int = None
    useItemNum1: int = None
    useItemMstId2: int = None
    useItemNum2: int = None
    useItemMstId3: int = None
    useItemNum3: int = None
    conditionType: int = None
    conditionValue: int = None
class StyleStyleParamUpMstRecord(BaseModel):
    styleParamUpMstId: int = None
    groupId: int = None
    styleMstId: int = None
    styleParamUpTreeMstId: int = None
    priority: int = None
    isStyleUniqueEffect: bool = None
    styleParamUpEffectMstId: int = None
    styleParamUpCostMstId: int = None
    useMoney: int = None
    useItemMstId1: int = None
    useItemNum1: int = None
    useItemMstId2: int = None
    useItemNum2: int = None
    useItemMstId3: int = None
    useItemNum3: int = None
    startTime: str = None
class StyleStyleParamUpCostMstRecord(BaseModel):
    styleParamUpCostMstId: int = None
    useMoney: int = None
    useItemMstId1: int = None
    useItemNum1: int = None
    useItemMstId2: int = None
    useItemNum2: int = None
    useItemMstId3: int = None
    useItemNum3: int = None
    useItemMstId4: int = None
    useItemNum4: int = None
    useItemMstId5: int = None
    useItemNum5: int = None
    useItemMstId6: int = None
    useItemNum6: int = None
    useItemMstId7: int = None
    useItemNum7: int = None
    useItemMstId8: int = None
    useItemNum8: int = None
class StyleStyleParamUpEffectMstRecord(BaseModel):
    styleParamUpEffectMstId: int = None
    name: str = None
    targetType: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
class StyleStyleLimitBreakMstRecord(BaseModel):
    styleLimitBreakMstId: int = None
    styleMstId: int = None
    limitBreakCount: int = None
    styleLimitBreakEffectMstId1: int = None
    styleLimitBreakEffectMstId2: int = None
class StyleStyleLimitBreakEffectMstRecord(BaseModel):
    styleLimitBreakEffectMstId: int = None
    name: str = None
    targetType: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
class StyleStyleLevelUpMstRecord(BaseModel):
    styleLevelUpMstId: int = None
    styleMstId: int = None
    level: int = None
    maxHp: int = None
    maxAtk: int = None
    maxDef: int = None
class StyleStyleVoiceMstRecord(BaseModel):
    styleVoiceMstId: int = None
    styleMstId: int = None
    name: str = None
    soundMstId: int = None
class GvgGvgPointRewardMstRecord(BaseModel):
    gvgPointRewardMstId: int = None
    point: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class GvgGvgRankingRewardMstRecord(BaseModel):
    gvgRankingRewardMstId: int = None
    leagueId: int = None
    ranking: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ChatChatStampMstRecord(BaseModel):
    chatStampMstId: int = None
    description: str = None
class QuestBattleBattleConditionMstRecord(BaseModel):
    battleConditionMstId: int = None
    description: str = None
    compareTarget: int = None
    compareContent: int = None
    compareOperator: int = None
    compareValue: str = None
class QuestBattleBattleConditionSetMstRecord(BaseModel):
    battleConditionSetMstId: int = None
    description: str = None
    battleConditionMstIdCsv: str = None
class QuestBattleEnemyConditionSetsAndActionMstRecord(BaseModel):
    enemyConditionSetsAndActionMstId: int = None
    questEnemyAppearanceMstId: int = None
    enemyConditionSkillSetId: int = None
    conditionSetMstIdCsv: str = None
    skillMstIdCsv: str = None
    isSkillBundle: bool = None
    isSkillReusable: bool = None
    priority: int = None
class CollectionDioramaBackgroundMstRecord(BaseModel):
    dioramaBackgroundMstId: int = None
    seriesId: int = None
    fieldSeriesMstId: int = None
    stageThumbnailName: str = None
    backgroundResourceName: str = None
    stageName: str = None
    unlockType: int = None
    unlockId: int = None
    releaseTime: str = None
    sortOrder: int = None
    enemyType: int = None
class CollectionLive2DParamMstRecord(BaseModel):
    live2DParamMstId: int = None
    _json: str = Field(alias='json')
class GvgGvgMstRecord(BaseModel):
    gvgMstId: int = None
    eventStartTime: str = None
    eventEndTime: str = None
    battleStartTime: str = None
    battleEndTime: str = None
    resourceName: str = None
    stagePrefabName: str = None
    bgmCueSheetName: str = None
    bgmCueName: str = None
class SoundSoundMstRecord(BaseModel):
    soundMstId: int = None
    seriesId: int = None
    soundType: int = None
    name: str = None
    songWriter: str = None
    songComposer: str = None
    cueSheetName: str = None
    cueName: str = None
    unlockType: int = None
    unlockId: int = None
    releaseTime: str = None
class SoundStreamableBgmMstRecord(BaseModel):
    streamableBgmMstId: int = None
    cueSheetName: str = None
    cueName: str = None
class CollectionCollectionIllustMstRecord(BaseModel):
    collectionIllustMstId: int = None
    name: str = None
    illustrator: str = None
    source: str = None
    questMapMstId: int = None
    completeRewardCardMstId: int = None
    completeRewardStyleMstId: int = None
    completeRewardGemNum: int = None
    completeHomeAppealMstId: int = None
    expandCelestialGlobe: bool = None
    resourceName: str = None
    isAutoUnlocked: bool = None
    advMstId: int = None
class CollectionCollectionIllustPieceMstRecord(BaseModel):
    collectionIllustPieceMstId: int = None
    collectionIllustMstId: int = None
    collectionConditionGroupMstId: int = None
class CollectionCollectionParamUpMstRecord(BaseModel):
    collectionParamUpMstId: int = None
    category: int = None
class CollectionCollectionParamUpLevelMstRecord(BaseModel):
    collectionParamUpLevelMstId: int = None
    collectionParamUpMstId: int = None
    level: int = None
    conditionCount: int = None
    paramUpText: str = None
    effectGroupId: int = None
    rewardGroupId: int = None
class CollectionCollectionParamUpEffectMstRecord(BaseModel):
    collectionParamUpEffectMstId: int = None
    effectGroupId: int = None
    targetType: int = None
    element: int = None
    stance: int = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
class CollectionCollectionConditionGroupMstRecord(BaseModel):
    collectionConditionGroupMstId: int = None
    fieldSeriesMstId: int = None
    conditionGroupId1: int = None
    conditionGroupId2: int = None
    advMstId1: int = None
    advMstId2: int = None
class CollectionCollectionConditionMstRecord(BaseModel):
    collectionConditionMstId: int = None
    conditionGroupId: int = None
    fieldPointMstId: int = None
    objectType: int = None
    objectId: int = None
    fieldSeriesMstId: int = None
    fieldStratumMstId: int = None
    fieldStageMstId: int = None
    stratumNum: int = None
    chapterNum: int = None
    dungeonEventMstId: int = None
    presetEventMstId: str = None
    collectionGroup: int = None
    groupType: int = None
    collectionIllustMstId: int = None
class CollectionCollectionRewardMstRecord(BaseModel):
    collectionRewardMstId: int = None
    rewardGroupId: int = None
    sortOrder: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class StoryEventStoryEventMstRecord(BaseModel):
    storyEventMstId: int = None
    name: str = None
    storyQuestGroupId: int = None
    scoreAttackMstId: int = None
    maxPlayCountPerDay: int = None
    eventItemId: int = None
    shopSeriesMstId: int = None
    bonusStyleIds: str = None
    isEndPlayable: bool = None
    endDisplayTime: str = None
    sortOrder: int = None
    eventStartDirection: int = None
    topImageName: str = None
    bannerImageName: str = None
    bossCameraAssetName: str = None
    description: str = None
    soundMstId: int = None
class StoryEventStoryEventQuestStageMstRecord(BaseModel):
    questStageMstId: int = None
    eventItemNum: int = None
    filmNo: int = None
class TutorialMiniTutorialMstRecord(BaseModel):
    miniTutorialMstId: int = None
    miniTutorialNumber: int = None
    sortOrder: int = None
    title: str = None
    description: str = None
    resourceName: str = None
    advMstId: int = None
class StoryEventStoryEventScenarioMstRecord(BaseModel):
    storyEventScenarioMstId: int = None
    storyEventMstId: int = None
    advMstId: int = None
    conditionQuestStageMstId: int = None
    conditionScenarioMstId: int = None
    sortOrder: int = None
    filmNo: int = None
    viewType: int = None
class StoryEventStoryEventScenarioRewardMstRecord(BaseModel):
    storyEventScenarioRewardMstId: int = None
    storyEventScenarioMstId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class StoryEventStoryEventBonusRateMstRecord(BaseModel):
    storyEventBonusRateMstId: int = None
    storyEventMstId: int = None
    bonusType: int = None
    bonusMstId: int = None
    limitBreakCount0Rate: int = None
    limitBreakCount1Rate: int = None
    limitBreakCount2Rate: int = None
    limitBreakCount3Rate: int = None
    limitBreakCount4Rate: int = None
    limitBreakCount5Rate: int = None
class DungeonDungeonMstRecord(BaseModel):
    dungeonMstId: int = None
    questGroupMstId: int = None
    dungeonTypeMstId: int = None
    dungeonName: str = None
    characterResourceName: str = None
    resourceName: str = None
    recommendationElementCsv: str = None
    recommendationPartyPower: int = None
    soundMstId: int = None
    recommendationElement: int = None
class DungeonDungeonTypeMstRecord(BaseModel):
    dungeonTypeMstId: int = None
    structureType: int = None
    room1LengthType: int = None
    room2LengthType: int = None
    room3LengthType: int = None
    room4LengthType: int = None
    room5LengthType: int = None
class DungeonDungeonRoomMstRecord(BaseModel):
    dungeonRoomMstId: int = None
    dungeonMstId: int = None
    roomIndex: int = None
    cameraType: int = None
    presetEvent1: int = None
    presetEvent2: int = None
    presetEvent3: int = None
    presetEvent4: int = None
    presetEvent5: int = None
    levelResourceName: str = None
    backgroundResourceName: str = None
class DungeonDungeonEventMstRecord(BaseModel):
    dungeonEventMstId: int = None
    dungeonRoomMstId: int = None
    dungeonMstId: int = None
    dungeonPointId: int = None
    eventType: int = None
    value1: int = None
    value2: int = None
    value3: int = None
    value4: int = None
    isHidden: bool = None
    dungeonRoomId: int = None
    order: int = None
class ExplorationFieldStratumMstRecord(BaseModel):
    fieldStratumMstId: int = None
    fieldStageMstId: int = None
    stratumNum: int = None
    isWholeFieldVisible: bool = None
    soundMstId: int = None
    stratumName: str = None
class ExplorationFieldPointMstRecord(BaseModel):
    fieldPointMstId: int = None
    fieldStratumMstId: int = None
    prevFieldPointMstId: int = None
    name: str = None
    chapterNum: int = None
    pointType: int = None
    pointValue1: int = None
    pointValue2: int = None
    displayType: int = None
    isHidden: bool = None
    firstClearRewardGroupId: int = None
    firstClearOtherCollectionRewardGroupId: int = None
    needViewAdvMstIds: str = None
    coordinateId: int = None
    assetbundleName: str = None
    startTime: str = None
class ExplorationBossDirectionMstRecord(BaseModel):
    bossDirectionMstId: int = None
    resourceName: str = None
    nextSceneType: int = None
    objectId: int = None
    nextBossDirectionMstId: int = None
class GatheringGatheringLevelMstRecord(BaseModel):
    gatheringLevel: int = None
    userLevel: int = None
class GatheringGatheringRewardMstRecord(BaseModel):
    gatheringRewardMstId: int = None
    gatheringLevel: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    startTime: str = None
    endTime: str = None
class ScoreAttackScoreAttackMstRecord(BaseModel):
    scoreAttackMstId: int = None
    name: str = None
    startTime: str = None
    endTime: str = None
    comment: str = None
    reprintNum: int = None
    highScoreRewardGroupId: int = None
    totalScoreRewardGroupId: int = None
    rankingRewardGroupId: int = None
    dioramaBackgroundMstId: int = None
class ScoreAttackScoreAttackStageMstRecord(BaseModel):
    scoreAttackStageMstId: int = None
    scoreAttackMstId: int = None
    questStageMstId: int = None
    difficulty: int = None
    dioramaBackgroundMstId: int = None
    comment: str = None
class ScoreAttackScoreAttackHighScoreRewardMstRecord(BaseModel):
    scoreAttackHighScoreRewardMstId: int = None
    groupId: int = None
    score: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ScoreAttackScoreAttackTotalScoreRewardMstRecord(BaseModel):
    scoreAttackTotalScoreRewardMstId: int = None
    groupId: int = None
    score: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ScoreAttackScoreAttackRankingRewardMstRecord(BaseModel):
    scoreAttackRankingRewardMstId: int = None
    groupId: int = None
    ranking: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class CalcPointCalculationPointPolicyMstRecord(BaseModel):
    calculationPointPolicyMstId: int = None
    policyType: int = None
    coefficientName: str = None
    conditionValue: int = None
    value: int = None
    startTime: str = None
class GuildMissionGuildMissionMstRecord(BaseModel):
    guildMissionMstId: int = None
    missionTitleMstId: int = None
    sortOrder: int = None
    guildMissionUniqueId: int = None
    guildMissionUniquePriority: int = None
    title: str = None
    description: str = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    resetType: int = None
    resetCycle: int = None
    triggerType: int = None
    conditionType: int = None
    conditionObjectId: int = None
    conditionObjectId2: int = None
    conditionCount: int = None
    startTime: str = None
    endTime: str = None
class GuildMissionGuildMissionTransitionMstRecord(BaseModel):
    guildMissionTransitionMstId: int = None
    guildMissionMstId: int = None
    transitionSceneName: str = None
    transitionSceneParam: int = None
class MovieMovieReplaceMstRecord(BaseModel):
    movieReplaceMstId: int = None
    path: str = None
    isStreamable: bool = None
    bgmOffPath: str = None
    englishPath: str = None
    bgmOffEnglishPath: str = None
class QuestOutGameQuestMissionMstRecord(BaseModel):
    questMissionMstId: int = None
    questMissionGroupId: int = None
    sortOrder: int = None
    conditionType: int = None
    conditionCount: int = None
class SelectionAbilitySelectionAbilityMstRecord(BaseModel):
    selectionAbilityMstId: int = None
    selectionAbilityType: int = None
    selectionAbilityEffectId: int = None
    rarity: int = None
    targetType: int = None
    name: str = None
    description: str = None
    abilityEffectType: str = None
    value1: int = None
    value2: int = None
    styleMstId: int = None
    resourceIconName: str = None
    sortOrder: int = None
class SelectionAbilitySelectionAbilityLotteryMstRecord(BaseModel):
    selectionAbilityLotteryMstId: int = None
    selectionAbilityLotteryGroupId: int = None
    selectionAbilityType: int = None
class SelectionAbilitySelectionAbilityLotteryRateMstRecord(BaseModel):
    selectionAbilityLotteryGroupId: int = None
    objectId: int = None
class SteamSteamAchievementMstRecord(BaseModel):
    steamAchievementMstId: int = None
    apiName: str = None
    conditionType: int = None
    conditionId: int = None
    achievementValueType: int = None
    max: int = None
    releaseTime: str = None
class QuestOutGameQuestCampaignMstRecord(BaseModel):
    questCampaignMstId: int = None
    questMapMstId: int = None
    campaignType: int = None
    campaignValue: int = None
    startTime: str = None
    endTime: str = None
    description: str = None
class MultiRaidMultiRaidMstRecord(BaseModel):
    multiRaidMstId: int = None
    seasonId: int = None
    startTime: str = None
    endTime: str = None
    multiRaidBattleBonusGroupId: int = None
    dailyBonusLotteryRarityGroupId: int = None
class MultiRaidMultiRaidStageMstRecord(BaseModel):
    multiRaidStageMstId: int = None
    seasonId: int = None
    questStageMstId: int = None
    difficulty: int = None
    limitRoundCount: int = None
    questRewardGroupId: int = None
    scoreRewardGroupId: int = None
    loseRewardGroupId: int = None
    useStaminaForPlay: int = None
    useStaminaForRescue: int = None
    dioramaBackgroundMstId: int = None
    comment: str = None
class MultiRaidMultiRaidBattleBonusMstRecord(BaseModel):
    multiRaidBattleBonusMstId: int = None
    passiveSkillMstId: int = None
    groupId: int = None
class MultiRaidMultiRaidDailyBonusRewardMstRecord(BaseModel):
    multiRaidDailyBonusRewardMstId: int = None
    groupId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class MultiRaidMultiRaidScoreRewardMstRecord(BaseModel):
    multiRaidScoreRewardMstId: int = None
    groupId: int = None
    rank: int = None
    questRewardGroupId: int = None
class MultiRaidMultiRaidLoseRewardMstRecord(BaseModel):
    multiRaidLoseRewardMstId: int = None
    groupId: int = None
    rank: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class MapGveMapGveUserDataRecord(BaseModel):
    userId: int = None
    mapGveMstId: int = None
    mapGvePointMstId: int = None
    enableMovePointMstIdCsv: str = None
    clearPointMstIdCsv: str = None
    unlockPointMstIdCsv: str = None
    totalDamage: int = None
class MapGveMapGveGuildDataRecord(BaseModel):
    guildDataId: int = None
    mapGveMstId: int = None
    reachBossPointMstIdCsv: str = None
class MapGveMapGveRankingRecord(BaseModel):
    userName: str = None
    rank: int = None
    ranking: int = None
    totalDamage: int = None
    favoriteStyleMstId: int = None
class CardCardDataRecord(BaseModel):
    userId: int = None
    cardDataId: int = None
    cardMstId: int = None
    passiveSkillLevel: int = None
    limitBreakCount: int = None
    isProtect: bool = None
    isAlreadyView: bool = None
    createdTime: str = None
class ItemItemDataRecord(BaseModel):
    userId: int = None
    itemMstId: int = None
    lotNumber: int = None
    num: int = None
    endTime: str = None
class CharacterCharacterDataRecord(BaseModel):
    userId: int = None
    characterMstId: int = None
    awakeLevel: int = None
    level: int = None
    exp: int = None
    heartLevel: int = None
    heartExp: int = None
    intimacyPoint: int = None
    useCount: int = None
    levelResetCount: int = None
    createdTime: str = None
class StyleSkillInfo(BaseModel):
    skillMstId: int = None
    skillUniqueId: int = None
    level: int = None
class StylePassiveSkillInfo(BaseModel):
    passiveSkillMstId: int = None
    skillUniqueId: int = None
    level: int = None
class StyleSpecialAttackSkillInfo(BaseModel):
    skillMstId: int = None
    level: int = None
    maxLevel: int = None
class StyleLeaderSkillInfo(BaseModel):
    leaderSkillMstId: int = None
    level: int = None
class StyleParamUpTreeInfo(BaseModel):
    styleParamUpTreeMstId: int = None
    isOpen: bool = None
    lastParamUpPriority: int = None
class StyleParamUpEffectInfo(BaseModel):
    abilityEffectType: str = None
    totalValue1: int = None
    totalValue2: int = None
class StyleStyleDataRecord(BaseModel):
    userId: int = None
    styleMstId: int = None
    level: int = None
    exp: int = None
    limitBreakCount: int = None
    specialAttackLevel: int = None
    normalAttackLevel: int = None
    skill1Level: int = None
    passiveSkill1Level: int = None
    limitBreakPassiveSkill1Level: int = None
    createdTime: str = None
    normalAttackInfo: StyleSkillInfo = None
    skillInfoList: List[StyleSkillInfo] = None
    passiveSkillInfoList: List[StylePassiveSkillInfo] = None
    limitBreakPassiveSkillInfoList: List[StylePassiveSkillInfo] = None
    selectionAbilityPassiveSkillInfoList: List[StylePassiveSkillInfo] = None
    subPassiveSkillInfo: StylePassiveSkillInfo = None
    specialAttackSkillInfo: StyleSpecialAttackSkillInfo = None
    leaderSkillInfo: StyleLeaderSkillInfo = None
    paramUpTreeInfoList: List[StyleParamUpTreeInfo] = None
    lastParamUpPriority: int = None
    paramUpEffectInfoList: List[StyleParamUpEffectInfo] = None
    limitBreakParamUpEffectInfoList: List[StyleParamUpEffectInfo] = None
    selectionAbilityParamUpEffectInfoList: List[StyleParamUpEffectInfo] = None
    isAlreadyView: bool = None
class CollectionCollectionDataRecord(BaseModel):
    userId: int = None
    objectType: ObjectObjectType = None
    objectId: int = None
    isGet: bool = None
    isAlreadyView: bool = None
    createdTime: str = None
class ObjectObjectViewData(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ObjectStyleGainViewData(BaseModel):
    styleMstId: int = None
    num: int = None
    isNew: bool = None
    convertedItem: ObjectObjectViewData = None
    additionObjectList: List[ObjectObjectViewData] = None
class ObjectCardGainViewData(BaseModel):
    cardMstId: int = None
    num: int = None
    isNew: bool = None
    convertedItem: ObjectObjectViewData = None
class ObjectGainViewData(BaseModel):
    styleGainViewDataList: List[ObjectStyleGainViewData] = None
    cardGainViewDataList: List[ObjectCardGainViewData] = None
class ObjectObjectDataRecord(BaseModel):
    cardDataList: List[CardCardDataRecord] = None
    itemDataList: List[ItemItemDataRecord] = None
    characterDataList: List[CharacterCharacterDataRecord] = None
    styleDataList: List[StyleStyleDataRecord] = None
    collectionDataList: List[CollectionCollectionDataRecord] = None
    talismanDataList: List[TalismanTalismanDataRecord] = None
    userParamData: UserUserParamDataRecord = None
    gainViewData: ObjectGainViewData = None
class InAppSnsAccessToken(BaseModel):
    accessToken: str = None
    accountId: str = None
class HariboteChatMessageDataRecord(BaseModel):
    userName: str = None
    userId: int = None
    styleMstId: int = None
    message: str = None
    createdTime: str = None
class QuestBattleQuestRoomData(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    gveStageMstId: int = None
    fieldStageMstId: int = None
    backGroundPlay: bool = None
    repeatNum: int = None
    createdTime: str = None
class ExplorationFieldStageUserDataRecord(BaseModel):
    userId: int = None
    fieldSeriesMstId: int = None
    fieldStageMstId: int = None
    fieldPointMstId: int = None
    dungeonPointId: int = None
    presetEventMstId: str = None
    enableMoveFieldPointMstIdCsv: str = None
    clearFieldPointMstIdCsv: str = None
    clearTempDungeonEventMstIdCsv: str = None
    clearTempPresetEventMstIdCsv: str = None
    clearDungeonEventMstIdCsv: str = None
    clearPresetEventMstIdCsv: str = None
    openFieldPointMstIdCsv: str = None
    isClear: bool = None
    firstBattleFieldStratumMstIdCsv: str = None
class CharacterCharacterLevelUpInfo(BaseModel):
    characterMstId: int = None
    styleMstId: int = None
    beforeLevel: int = None
    beforeExp: int = None
    afterLevel: int = None
    afterExp: int = None
class StyleStyleLevelUpInfo(BaseModel):
    styleMstId: int = None
    beforeLevel: int = None
    beforeExp: int = None
    afterLevel: int = None
    afterExp: int = None
class CollectionCollectionDetailInfo(BaseModel):
    groupType: int = None
    groupValue: int = None
    isBossStratum: bool = None
    group1ConditionCount: int = None
    group2ConditionCount: int = None
    group1AchievedCount: int = None
    group2AchievedCount: int = None
class CollectionFieldStageCollectionInfo(BaseModel):
    fieldStageMstId: int = None
    enableEntry: bool = None
    isClear: bool = None
    maxReleasedStratumNum: int = None
    collectionIllustMstId: int = None
    group1ConditionCount: int = None
    group2ConditionCount: int = None
    group1AchievedCount: int = None
    group2AchievedCount: int = None
    itemConditionCount: int = None
    itemAchievedCount: int = None
    collectionDetailInfoList: List[CollectionCollectionDetailInfo] = None
class TutorialFeatureRelease(BaseModel):
    level: int = None
    featureReleaseStrList: List[str] = None
class TutorialMiniTutorialDataRecord(BaseModel):
    userId: int = None
    finishedMiniTutorialNumberList: List[int] = None
class QuestOutGameUserQuestMissionDataRecord(BaseModel):
    userId: int = None
    questStageMstId: int = None
    reprintNum: int = None
    questMissionMstId: int = None
    isClear: bool = None
    count: int = None
class ExplorationBattleQuestMissionInfo(BaseModel):
    questMissionMstId: int = None
    currentBattleCount: int = None
    isFirstClearCurrentBattle: bool = None
class ExplorationBattleStageInfo(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    fieldStageMstId: int = None
    endTime: str = None
class QuestBattleAttackInfo(BaseModel):
    skillMstId: int = None
    level: int = None
class QuestBattlePassiveSkillInfo(BaseModel):
    passiveSkillMstId: int = None
    level: int = None
    abilitySourceType: int = None
class QuestBattleLeaderSkillInfo(BaseModel):
    leaderSkillMstId: int = None
    level: int = None
class QuestBattleTalismanParamInfo(BaseModel):
    talismanParamMstId: int = None
class QuestBattleBattleUnit(BaseModel):
    battleUnitDataId: int = None
    battleUnitType: int = None
    battleUnitMstId: int = None
    styleMstId: int = None
    levelReactionValue: int = None
    levelReactionBreakDamageValue: int = None
    levelReactionSlipDamageValue: int = None
    maxHp: int = None
    atk: int = None
    _def: int = Field(alias='def')
    speed: int = None
    criticalRate: int = None
    criticalDamageRate: int = None
    breakDamageRate: int = None
    healRate: int = None
    recoveryEpRate: int = None
    effectHitRate: int = None
    effectParryRate: int = None
    fireDamageRate: int = None
    aquaDamageRate: int = None
    forestDamageRate: int = None
    lightDamageRate: int = None
    darkDamageRate: int = None
    neutralDamageRate: int = None
    fireResistRate: int = None
    aquaResistRate: int = None
    forestResistRate: int = None
    lightResistRate: int = None
    darkResistRate: int = None
    neutralResistRate: int = None
    normalAttackInfo: QuestBattleAttackInfo = None
    attackInfoList: List[QuestBattleAttackInfo] = None
    specialAttackInfo: QuestBattleAttackInfo = None
    passiveSkillInfoList: List[QuestBattlePassiveSkillInfo] = None
    leaderSkillInfo: QuestBattleLeaderSkillInfo = None
    talismanParamInfoList: List[QuestBattleTalismanParamInfo] = None
class SelectionAbilitySelectionAbilityDataRecord(BaseModel):
    styleMstId: int = None
    userId: int = None
    mainSelectionAbilityMstId1: int = None
    mainSelectionAbilityMstId2: int = None
    mainSelectionAbilityMstId3: int = None
    mainSelectionAbilityMstId4: int = None
    mainSelectionAbilityMstId5: int = None
    mainSelectionAbilityMstId2Enabled: bool = None
    mainSelectionAbilityMstId3Enabled: bool = None
    mainSelectionAbilityMstId4Enabled: bool = None
    mainSelectionAbilityMstId5Enabled: bool = None
    subSelectionAbilityMstIds1: str = None
    subSelectionLocks1: str = None
    subSelectionTempLocksReserved1: str = None
    subSelectionAbilityMstIds2: str = None
    subSelectionLocks2: str = None
    subSelectionTempLocksReserved2: str = None
    subSelectionAbilityMstIds3: str = None
    subSelectionLocks3: str = None
    subSelectionTempLocksReserved3: str = None
    subSelectionAbilityMstIds4: str = None
    subSelectionLocks4: str = None
    subSelectionTempLocksReserved4: str = None
    subSelectionAbilityMstIds5: str = None
    subSelectionLocks5: str = None
    subSelectionTempLocksReserved5: str = None
    stockSelectionAbilityMstIds: str = None
    updatedTime: str = None
class PartyCharacterBuildDetail(BaseModel):
    styleData: StyleStyleDataRecord = None
    characterData: CharacterCharacterDataRecord = None
    cardData: CardCardDataRecord = None
    cardDataList: List[CardCardDataRecord] = None
    talismanDataList: List[TalismanTalismanDataRecord] = None
    subStyleDataList: List[StyleStyleDataRecord] = None
    subStyleCharacterDataList: List[CharacterCharacterDataRecord] = None
    subCardDataList: List[CardCardDataRecord] = None
    selectionAbilityData: SelectionAbilitySelectionAbilityDataRecord = None
class AppVersionAppealTitleInfo(BaseModel):
    titleResourceName: str = None
    homeResourceName: str = None
    startTime: str = None
    endTime: str = None
class TowerUserTowerDataRecord(BaseModel):
    userId: int = None
    eventType: int = None
    maxQuestStageMstId: int = None
    skipNum: int = None
    skipNumUpdatedTime: str = None
    skipNumForItem: int = None
    skipNumForItemRecoverInADay: int = None
    skipNumForItemRecoverTime: str = None
    reprintNum: int = None
class TowerSkipFloorDataRecord(BaseModel):
    prevMaxQuestStageMstId: int = None
    rewardMstIds: List[int] = None
    objectDataRecord: ObjectObjectDataRecord = None
class QuestOutGameUserQuestStageDataRecord(BaseModel):
    userId: int = None
    questStageMstId: int = None
    reprintNum: int = None
    questGroupMstId: int = None
    lastElapsedSeconds: int = None
    clearCount: int = None
    dailyClearCount: int = None
    dailyClearCountUpdatedTime: str = None
class StoryEventStoryEventDataRecord(BaseModel):
    userId: int = None
    storyEventMstId: int = None
    todayPlayableCount: int = None
    gemRecoveryCount: int = None
    countResetTime: str = None
class StoryEventStoryEventInfo(BaseModel):
    storyEventMstId: int = None
    startTime: str = None
    endTime: str = None
    isOpen: bool = None
    isUnlocked: bool = None
    isPlayable: bool = None
    openForceScenarioMstId: int = None
class QuestOutGameUserQuestGroupDataRecord(BaseModel):
    userId: int = None
    questGroupMstId: int = None
    startTime: str = None
    endTime: str = None
class ScoreAttackUserScoreAttackDataRecord(BaseModel):
    scoreAttackMstId: int = None
    userId: int = None
    highScore: int = None
    totalScore: int = None
    questStageMstId: int = None
    scoreAttackHighScoreRewardMstId: int = None
    scoreAttackTotalScoreRewardMstId: int = None
    reprintNum: int = None
    clearedDifficulty: int = None
class ShopShopCountDataRecord(BaseModel):
    userId: int = None
    shopSeriesMstId: int = None
    shopMstId: int = None
    purchaseCount: int = None
    resetTime: str = None
class ShopBuyViewData(BaseModel):
    isSuccess: bool = None
class ShopReceivedObjectData(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    isSendPresent: bool = None
class ShopShopPaymentMstRecord(BaseModel):
    shopPaymentMstId: int = None
    groupId: int = None
    productId: str = None
    type: int = None
    announceMstId: int = None
    name: str = None
    description: str = None
    isSale: bool = None
    comment: str = None
    startTime: str = None
    endTime: str = None
    resourceName: str = None
    dispType: int = None
class ShopShopPaymentBonusRewardMstRecord(BaseModel):
    shopPaymentBonusRewardMstId: int = None
    groupId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class ShopSubscriptionDescriptionRecord(BaseModel):
    label: str = None
    rewardDetailAnnounceMstId: int = None
    description: List[str] = None
    notesIos: List[str] = None
    notesAndroid: List[str] = None
class SelectionAbilitySelectionAbilityConversionItemData(BaseModel):
    styleMstId: int = None
    selectionAbilityMstId: int = None
    conversionSelectionAbilityMstId: int = None
    conversionItemMstId: int = None
    conversionItemNum: int = None
class ScoreAttackRankingInfo(BaseModel):
    userName: str = None
    userId: int = None
    rank: int = None
    ranking: int = None
    score: int = None
    favoriteStyleMstId: int = None
    setUserTitleMstIds: str = None
    partyPower: int = None
class ScoreAttackScoreAttackRoomData(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    scoreAttackStageMstId: int = None
    endTime: str = None
    createdTime: str = None
class ScoreAttackStageInfo(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    scoreAttackStageMstId: int = None
    endTime: str = None
class ScoreAttackScoreInfo(BaseModel):
    score: int = None
    roundBonus: int = None
    difficultyBonus: int = None
    turnDamageBonus: int = None
    roundDamageBonus: int = None
    hpBonus: int = None
    aliveBonus: int = None
    roundCount: int = None
    difficulty: int = None
    maxTurnDamage: int = None
    maxRoundDamage: int = None
    battleEndHp: int = None
    maxHp: int = None
    aliveCount: int = None
class PvpPvpTopInfo(BaseModel):
    selfRanking: int = None
    selfPvpPoint: int = None
    winStreakCount: int = None
    remainTodayFreePlayCount: int = None
    remainTodayPlayCount: int = None
    seasonId: int = None
    startTime: str = None
    endTime: str = None
    nextSeasonStartTime: str = None
class PvpRankingInfo(BaseModel):
    userName: str = None
    userId: int = None
    rank: int = None
    ranking: int = None
    pvpPoint: int = None
    favoriteStyleMstId: int = None
    setUserTitleMstIds: str = None
    partyPower: int = None
class PvpCharacterBuildInfo(BaseModel):
    styleMstId: int = None
    partyIndex: int = None
    totalPower: int = None
class PvpPvpUserInfo(BaseModel):
    userId: int = None
    userName: str = None
    rank: int = None
    ranking: int = None
    point: int = None
    partyPower: int = None
    iconStyleMstId: int = None
    setUserTitleMstIds: str = None
    relativelyLevel: int = None
    characterBuildInfoList: List[PvpCharacterBuildInfo] = None
class PvpPointInfo(BaseModel):
    point: int = None
    basePoint: int = None
    relativelyBonus: int = None
    roundBonus: int = None
    hpBonus: int = None
    battleEndHp: int = None
    maxHp: int = None
    winStreakBonusCoefficient: float = None
class PvpRewardInfo(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class PvpMatchHistory(BaseModel):
    pvpDataId: int = None
    result: int = None
    addPoint: int = None
    offenseUserId: int = None
    offensePlayerName: str = None
    offensePlayerRank: int = None
    offensePartyPower: int = None
    offenseIconStyleMstId: int = None
    offenseSetUserTitleMstIds: str = None
    offenseBeforeRanking: int = None
    defenseUserId: int = None
    isDeletedAccount: bool = None
    defensePlayerName: str = None
    defensePlayerRank: int = None
    defensePartyPower: int = None
    defenseIconStyleMstId: int = None
    defenseSetUserTitleMstIds: str = None
    defenseBeforeRanking: int = None
class UserTitleUserTitleDataRecord(BaseModel):
    userId: int = None
    userTitleMstId: int = None
    value1: int = None
    createdTime: str = None
class PartyCharacterBuildDataRecord(BaseModel):
    userId: int = None
    styleMstId: int = None
    cardMstId: int = None
    subStyleMstIds: str = None
class UserUserProfileDataRecord(BaseModel):
    userId: int = None
    comment: str = None
    setUserTitleMstIds: str = None
    favoriteCharacterMstId: int = None
    favoriteSpecialAttackMstId: int = None
    pvpHighestRank: int = None
    continueLoginDayNum: int = None
    maxContinueLoginDayNum: int = None
    recentLoginTime: str = None
class CharacterUseCharacterRankingRecord(BaseModel):
    ranking: int = None
    characterMstId: int = None
    useCount: int = None
class GuildGuildDataRecord(BaseModel):
    guildDataId: int = None
    guildInstantId: int = None
    guildName: str = None
    guildMasterUserId: int = None
    guildMasterLevel: int = None
    guildMasterRecentLoginTime: str = None
    joinMember: int = None
    guildTitleMstId: int = None
    isAutoApproval: bool = None
    guildAtmosphere: int = None
    guildDescription: str = None
    lastGvgLeagueId: int = None
    lastGvgLeagueRanking: int = None
    totalMaxPartyPower: int = None
class GuildGuildRequestDataRecord(BaseModel):
    userId: int = None
    guildDataId: int = None
    requestType: int = None
    status: int = None
    sendTime: str = None
class CollectionCollectionParamUpAchieveDataRecord(BaseModel):
    userId: int = None
    collectionParamUpMstId: int = None
    achievedLevel: int = None
    viewedLevel: int = None
class UserHomeAppealLocalInfo(BaseModel):
    homeAppealMstId: int = None
    isViewed: bool = None
class UserEnhanceQuestUserLocalInfo(BaseModel):
    userId: int = None
    lastSelectedQuestRank: str = None
class UserMainQuestUserLocalInfo(BaseModel):
    userId: int = None
    latestUnlockedStageData: str = None
    enteredStageData: str = None
    lastPlayedFieldStageMstId: int = None
    lastPlayedQuestInfo: str = None
class UserStoryEventLocalInfo(BaseModel):
    dataLabel: str = None
    jsonParam: str = None
class UserSortInfo(BaseModel):
    sortType: str = None
    sortParameter: str = None
class UserSortDescInfo(BaseModel):
    sortDescType: str = None
    sortDescParameter: bool = None
class UserFilterInfo(BaseModel):
    filterType: str = None
    filterParameter: str = None
class UserUserDisplayInfo(BaseModel):
    userId: int = None
    name: str = None
    level: int = None
    favoriteStyleMstId: int = None
    recentLoginTime: str = None
    setUserTitleMstIds: str = None
    maxPartyPower: int = None
    isDeletedAccount: bool = None
class UserUserSubscriptionDataRecord(BaseModel):
    userId: int = None
    subscriptionLabel: str = None
    isSubscription: bool = None
    currentEndTime: str = None
    continueCount: int = None
class PresentPresentDataRecord(BaseModel):
    presentDataId: int = None
    userId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    comment: str = None
    receivedTime: str = None
    expireTime: str = None
    createdTime: str = None
class MultiRaidMultiRaidUserDataRecord(BaseModel):
    userId: int = None
    stamina: int = None
    staminaUpdatedTime: str = None
    recoveryCount: int = None
    recoveryResetTime: str = None
class MultiRaidMultiRaidUserSeasonDataRecord(BaseModel):
    userId: int = None
    seasonId: int = None
    todayPlayCount: int = None
    todayPlayCountResetTime: str = None
    todayClearedCount: int = None
    clearedDifficulty: int = None
    todayClearedDifficulty: int = None
class MultiRaidMultiRaidStageDataRecord(BaseModel):
    multiRaidStageDataId: int = None
    multiRaidStageMstId: int = None
    hostUserId: int = None
    hostUserName: str = None
    hostIconStyleMstId: int = None
    hostSetUserTitleMstIds: str = None
    hostIsGuildMember: bool = None
    hostIsDeletedAccount: bool = None
    hp: int = None
    isRescuedGuild: bool = None
    isRescuedAll: bool = None
    result: int = None
    endTime: str = None
    isClosed: bool = None
    createdTime: str = None
class MultiRaidMultiRaidRoomDataRecord(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    multiRaidStageDataId: int = None
    multiRaidStageMstId: int = None
    userId: int = None
    reprintNum: int = None
    partyDataId: int = None
    damage: int = None
    isClosed: bool = None
    result: int = None
    isReceivedReward: bool = None
    isReceivableDailyBonus: bool = None
    dailyBonusClearedDifficulty: int = None
    endTime: str = None
    createdTime: str = None
class UserUserLikeDataRecord(BaseModel):
    userId: int = None
    type: int = None
    count: int = None
class MultiRaidJoinUserInfo(BaseModel):
    userId: int = None
    userName: str = None
    level: int = None
    iconStyleMstId: int = None
    setUserTitleMstIds: str = None
    rank: int = None
    score: int = None
    isJoining: bool = None
    multiRaidStageDataId: int = None
    multiRaidStageMstId: int = None
    isGuildMember: bool = None
    isLiked: bool = None
    isDeletedAccount: bool = None
class MultiRaidRewardInfo(BaseModel):
    firstClearRewardMstIds: List[int] = None
    scoreRewardMstIds: List[int] = None
    hostClearRewardMstIds: List[int] = None
    loseRewardMstIds: List[int] = None
    dailyBonusRewardMstId: int = None
    additionalDailyBonusRewardMstId: int = None
    requiredScore: int = None
    dailyBonusRarity: int = None
class QuestBattleStageInfo(BaseModel):
    questDataId: int = None
    questStageMstId: int = None
    endTime: str = None
class MissionMissionDataRecord(BaseModel):
    userId: int = None
    missionUniqueId: int = None
    missionMstId: int = None
    resetTime: str = None
    count: int = None
    isClear: bool = None
    isClear2: bool = None
    isClear3: bool = None
    isDoubleBonus: bool = None
    isDoubleBonus2: bool = None
class GuildMissionGuildMissionDataRecord(BaseModel):
    guildDataId: int = None
    guildMissionUniqueId: int = None
    guildMissionMstId: int = None
    resetTime: str = None
    count: int = None
    isClear: bool = None
class GuildGuildUserDataRecord(BaseModel):
    userId: int = None
    guildDataId: int = None
    guildRoleMstId: int = None
    joinTime: str = None
class MissionreceivedObjectData(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    isSendPresent: bool = None
class PvpPvpResultRecord(BaseModel):
    userId: int = None
    lastRanking: int = None
    pvpPoint: int = None
    startTime: str = None
    endTime: str = None
    seasonId: int = None
class HomeHomeViewData(BaseModel):
    enablePresentBadge: bool = None
    enableMissionBadge: bool = None
    enableBeginnerMission: bool = None
    enableCollectionBadge: bool = None
    storyEventEndTime: str = None
    enableStoryEventBadge: bool = None
    towerFloorNum: int = None
    enableTowerBadge: bool = None
    enableMainQuestBadge: bool = None
    enableNewGachaBadge: bool = None
    enableFreeGachaBadge: bool = None
    enableGachaBadge: bool = None
    enableUnionBadge: bool = None
    enablePvpBadge: bool = None
    enableGvgBadge: bool = None
    characterHeartQuestPlayCount: int = None
    pvpResultInfo: PvpPvpResultRecord = None
    enableNewMultiRaidBadge: bool = None
    enablePlayMultiRaidBadge: bool = None
    multiRaidUserData: MultiRaidMultiRaidUserDataRecord = None
    multiRaidBattleStatus: int = None
    multiRaidLatestActivityTime: int = None
class HomeLoginBonusRecord(BaseModel):
    userId: int = None
    loginBonusMstId: int = None
    loginBonusRewardMstId: int = None
    dayCount: int = None
    dayTotalCount: int = None
    lastRewardDate: str = None
class UserComebackUserDataRecord(BaseModel):
    userId: int = None
    comebackCount: int = None
    comebackTime: str = None
    endTime: str = None
class UserUserLevelUpInfo(BaseModel):
    beforeLevel: int = None
    beforeExp: int = None
    beforeStamina: int = None
    userParamData: UserUserParamDataRecord = None
class GatheringUserGatheringDataRecord(BaseModel):
    userId: int = None
    gatheringLevel: int = None
    gatheringTime: str = None
    shortcutCount: int = None
    shortcutCountResetTime: str = None
class GvgGvgGuildInfo(BaseModel):
    ranking: int = None
    leagueId: int = None
    winNum: int = None
    dailyGuildPoint: int = None
    totalGuildPoint: int = None
    selfPoint: int = None
    isAggregation: bool = None
class GvgGvgEnemyGuildInfo(BaseModel):
    ranking: int = None
    guildName: str = None
    guildDataId: int = None
    guildTitleMstId: int = None
    dailyGuildPoint: int = None
class GvgMatchTopInfo(BaseModel):
    result: int = None
    addPoint: int = None
    userId: int = None
    playerName: str = None
class GvgMatchHistory(BaseModel):
    matchDateTime: str = None
    day: int = None
    result: int = None
    addPoint: int = None
    offenseUserId: int = None
    offensePlayerName: str = None
    offensePlayerRank: int = None
    offensePartyPower: int = None
    offenseIconStyleMstId: int = None
    offenseSetUserTitleMstIds: str = None
    defenseUserId: int = None
    defensePlayerName: str = None
    defensePlayerRank: int = None
    defensePartyPower: int = None
    defenseIconStyleMstId: int = None
    defenseSetUserTitleMstIds: str = None
    allyUserId: int = None
    allyPlayerName: str = None
    allyPlayerRank: int = None
    allyIconStyleMstId: int = None
    enemyUserId: int = None
    enemyPlayerName: str = None
    enemyPlayerRank: int = None
    enemyIconStyleMstId: int = None
class GvgMatchInfo(BaseModel):
    userId: int = None
    playerName: str = None
    playerRank: int = None
    iconStyleMstId: int = None
    setUserTitleMstIds: str = None
    partyPower: int = None
    relativelyLevel: int = None
    result: int = None
    characterBuildInfoList: List[PvpCharacterBuildInfo] = None
class GvgRankingInfo(BaseModel):
    guildDataId: int = None
    guildName: str = None
    ranking: int = None
    guildTitleMstId: int = None
    iconStyleMstId: int = None
    guildPoint: int = None
class GvgLeagueMatchResultInfo(BaseModel):
    guildDataId: int = None
    guild1Result: int = None
    guild2Result: int = None
    guild3Result: int = None
    guild4Result: int = None
class GvgLeagueMatchGuildInfo(BaseModel):
    guildName: str = None
    guildDataId: int = None
    guildTitleMstId: int = None
class GvgStageInfo(BaseModel):
    stagePrefabName: str = None
    bgmCueName: str = None
    bgmCueSheetName: str = None
class GveGveGuildDataRecord(BaseModel):
    guildDataId: int = None
    gveStageMstId: int = None
    chainId: int = None
    chainLevel: int = None
class GveGveUserDataRecord(BaseModel):
    userId: int = None
    todayPlayCount: int = None
    todayPlayCountResetTime: str = None
class GveGveStageDataRecord(BaseModel):
    guildDataId: int = None
    gveStageMstId: int = None
    hp: int = None
    breakCount: int = None
    isBreakBonus: bool = None
    isStrategyBuff: bool = None
    bossDebuffMag: int = None
class GveGveUserStageDataRecord(BaseModel):
    userId: int = None
    gveStageMstId: int = None
    useFirstBattleBreakBonus: bool = None
class GveGveGuildChainDataRecord(BaseModel):
    chainId: int = None
    chainLevel: int = None
    lastAttackTime: str = None
class GveRankingInfo(BaseModel):
    userId: int = None
    ranking: int = None
    damage: int = None
class GveGveHistoryInfo(BaseModel):
    userId: int = None
    attackTime: str = None
    damage: int = None
class GveGuildMemberCharacter(BaseModel):
    userId: int = None
    styleMstId: int = None
class GveGveUserChainDataRecord(BaseModel):
    userId: int = None
    chainId: int = None
    chainLevel: int = None
class GuildGuildTitleDataRecord(BaseModel):
    guildDataId: int = None
    guildTitleMstId: int = None
class GuildGuildActivityDataRecord(BaseModel):
    actionTime: str = None
    viewText: str = None
    userId: int = None
class GachaGachaRecord(BaseModel):
    gachaMstId: int = None
    gachaSeriesMstId: int = None
    gachaName: str = None
    payType: int = None
    payItemId: int = None
    price: int = None
    repeatCount: int = None
    countLimit: int = None
    dailyCountLimit: int = None
    minRarity: int = None
    minRarityCount: int = None
    startTime: str = None
    endTime: str = None
    sortNum: int = None
    ticketGachaMstId: int = None
class GachaGachaStepUpRecord(BaseModel):
    gachaSeriesMstId: int = None
    step: int = None
    gachaPickUpId: int = None
    payType: int = None
    price: int = None
    repeatCount: int = None
    minRarity: int = None
    minRarityCount: int = None
    sortNum: int = None
class GachaGachaSeriesRecord(BaseModel):
    gachaSeriesMstId: int = None
    name: str = None
    description: str = None
    headLine: str = None
    badgeType: int = None
    gachaType: GachaGachaType = None
    gachaDrawType: GachaGachaDrawType = None
    gachaRateId: int = None
    gachaPickUpId: int = None
    seriesCountLimit: int = None
    seriesDailyCountLimit: int = None
    lapLimit: int = None
    priority: int = None
    shopSeriesMstId: int = None
    bannerMstId: int = None
    resourceName: str = None
    bonusGachaSeriesMstId: int = None
class GachaGachaAppealRecord(BaseModel):
    gachaSeriesMstId: int = None
    movieResourceName1: str = None
    movieResourceName2: str = None
    movieResourceName3: str = None
    imageResourceName1: str = None
    imageResourceName2: str = None
    imageResourceName3: str = None
    imageResourceName4: str = None
    imageResourceName: str = None
    styleMstId1: int = None
    styleMstId2: int = None
    styleMstId3: int = None
    stampType1: int = None
    stampType2: int = None
    stampType3: int = None
class GachaGachaBonusRecord(BaseModel):
    gachaBonusMstId: int = None
    gachaMstId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class GachaGachaPickUpBonusRecord(BaseModel):
    gachaPickUpBonusMstId: int = None
    gachaSeriesMstId: int = None
    styleMstId: int = None
    gachaPickUpBonusGroupId: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
    priority: int = None
class GachaGachaSeriesBonusRecord(BaseModel):
    gachaSeriesBonusMstId: int = None
    gachaSeriesMstId: int = None
    gachaCount: int = None
    lap: int = None
    step: int = None
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class GachaGachaCountDataRecord(BaseModel):
    userId: int = None
    gachaMstId: int = None
    dailyCount: int = None
    totalCount: int = None
    resetTime: str = None
class ItemConversionItemViewByBeforeItem(BaseModel):
    bannerMstId: int = None
    beforeItemMstId: int = None
    beforeNum: int = None
    conversionNum: int = None
class ItemConversionItemViewByAfterItem(BaseModel):
    conversionItemMstId: int = None
class GachaGachaTopViewData(BaseModel):
    gachaList: List[GachaGachaRecord] = None
    gachaStepUpList: List[GachaGachaStepUpRecord] = None
    gachaSeriesList: List[GachaGachaSeriesRecord] = None
    gachaAppealList: List[GachaGachaAppealRecord] = None
    gachaBonusList: List[GachaGachaBonusRecord] = None
    gachaPickUpBonusList: List[GachaGachaPickUpBonusRecord] = None
    gachaSeriesBonusList: List[GachaGachaSeriesBonusRecord] = None
    gachaCountDataList: List[GachaGachaCountDataRecord] = None
    newBadgeGachaSeriesMstIdList: List[int] = None
    conversionItemViewByBeforeItemList: List[ItemConversionItemViewByBeforeItem] = None
    conversionItemViewByAfterItem: ItemConversionItemViewByAfterItem = None
    itemDataList: List[ItemItemDataRecord] = None
class GachaPickUpInfo(BaseModel):
    objectReceiveType: int = None
    objectType: int = None
    objectId: int = None
    gachaPickUpBonusGroupId: int = None
class GachaGachaGemTextInfo(BaseModel):
    gachaMstId: int = None
    text: str = None
class QuestOutGameUserQuestTrainingDataRecord(BaseModel):
    userId: int = None
    questGroupMstId: int = None
    clearedQuestStageMstId: int = None
    rankUpEffectedQuestStageMstId: int = None
class QuestOutGameUserQuestCharacterHeartDataRecord(BaseModel):
    userId: int = None
    dailyClearCount: int = None
    dailyClearCountUpdatedTime: str = None
class QuestOutGameUserQuestCharacterHeartPartySaveDataRecord(BaseModel):
    userId: int = None
    questStageMstId: int = None
    member1: int = None
    cardMstId1: int = None
    subStyleMstIds1: str = None
    member2: int = None
    cardMstId2: int = None
    subStyleMstIds2: str = None
    member3: int = None
    cardMstId3: int = None
    subStyleMstIds3: str = None
    member4: int = None
    cardMstId4: int = None
    subStyleMstIds4: str = None
    member5: int = None
    cardMstId5: int = None
    subStyleMstIds5: str = None
class LoginBonusLoginBonusConfig(BaseModel):
    loginBonusRefreshHour: int = None
class CharacterAwakeCostInfo(BaseModel):
    awakeLevel: int = None
    onlyMaterialNum: int = None
    genericMaterialNum: int = None
class CharacterRegionRecord(BaseModel):
    regionId: int = None
    name: str = None
class CharacterSeriesRecord(BaseModel):
    seriesId: int = None
    name: str = None
class CharacterLevelUpCost(BaseModel):
    level: int = None
    exp: int = None
    goldPerExp: int = None
class CharacterCharacterConfig(BaseModel):
    awakeCostInfo: List[CharacterAwakeCostInfo] = None
    region: List[CharacterRegionRecord] = None
    series: List[CharacterSeriesRecord] = None
    genericAwakeItemMstId: int = None
    namaeCharacterMstId: int = None
    namaeObjectRewardGroupId: int = None
    levelUpCost: List[CharacterLevelUpCost] = None
class CardCardGenericLimitBreakRecord(BaseModel):
    rarity: int = None
    itemMstId: int = None
class CardCardMaxLevelRecord(BaseModel):
    rarity: int = None
    limitBreakCount: int = None
    maxLevel: int = None
class CardCardSellRecord(BaseModel):
    rarity: int = None
    itemMstId: int = None
    num: int = None
    gold: int = None
class CardUnlockSubCardDataSlotRecord(BaseModel):
    achievedLevel: int = None
    slot: int = None
class CardSubCardReflectRateRecord(BaseModel):
    equippedNum: int = None
    rate: int = None
class CardCardLimitBreakRarityRecord(BaseModel):
    rarity: int = None
    itemMstId: int = None
    num: int = None
class CardCardConfig(BaseModel):
    genericLimitBreakInfo: List[CardCardGenericLimitBreakRecord] = None
    maxLevelInfo: List[CardCardMaxLevelRecord] = None
    sellCardInfo: List[CardCardSellRecord] = None
    unlockSubCardDataSlot: List[CardUnlockSubCardDataSlotRecord] = None
    subCardReflectRate: List[CardSubCardReflectRateRecord] = None
    cardLimitBreakRarityInfo: List[CardCardLimitBreakRarityRecord] = None
class CollectionCollectionConfig(BaseModel):
    gainGemNum: int = None
    hiddenGalleryCardMstIdList: List[int] = None
    notDispCollectionStyleFigureMstIds: List[int] = None
class StyleStyleLimitBreakRarityRecord(BaseModel):
    rarity: int = None
    itemMstId: int = None
    num: int = None
class StyleStyleLimitBreakCostRecord(BaseModel):
    rarity: int = None
    itemMstId: int = None
    num: int = None
class StyleLimitBreakBonusRecord(BaseModel):
    limitBreakCount: int = None
    bonus: int = None
class StyleLimitBreakCharacterMaxLevelRecord(BaseModel):
    rarity: int = None
    limitBreakCount: int = None
    maxLevel: int = None
class StyleUnlockSubStyleDataSlotRecord(BaseModel):
    achievedLevel: int = None
    styleLevel: int = None
    fieldStageMstId: int = None
    conditionTxt: str = None
    slot: int = None
    miniTutorialNumber: int = None
class StyleLimitBreakSpecialAttackMaxLevelRecord(BaseModel):
    limitBreakCount: int = None
    maxLevel: int = None
class StyleParamUpMaxPriorityInfo(BaseModel):
    styleLevel: int = None
    maxPriority: int = None
class StyleLevelUpCost(BaseModel):
    level: int = None
    exp: int = None
    goldPerExp: int = None
class StyleStyleConfig(BaseModel):
    styleLimitBreakRarityInfo: List[StyleStyleLimitBreakRarityRecord] = None
    limitBreakCostInfo: List[StyleStyleLimitBreakCostRecord] = None
    limitBreakBonus: List[StyleLimitBreakBonusRecord] = None
    limitBreakCharacterMaxLevel: List[StyleLimitBreakCharacterMaxLevelRecord] = None
    limitBreakPassiveSkill1TargetCount: int = None
    limitBreakSpecialAttackEffectTargetCount: int = None
    unlockSubStyleDataSlot: List[StyleUnlockSubStyleDataSlotRecord] = None
    maxSkillLevel: int = None
    defaultSpecialAttackMaxLevel: int = None
    limitBreakSpecialAttackMaxLevel: List[StyleLimitBreakSpecialAttackMaxLevelRecord] = None
    paramUpMaxPriorityInfo: List[StyleParamUpMaxPriorityInfo] = None
    levelUpCost: List[StyleLevelUpCost] = None
    unlockSubStyleFieldStageMstId: int = None
class PvpWinStreakBonusRate(BaseModel):
    winStreakCount: int = None
    correctedBonusRate: int = None
class PvpPvpConfig(BaseModel):
    maxFreePlayCountPerDay: int = None
    maxPlayCountPerDay: int = None
    addPlayCountGemNum: int = None
    outOfRangeRanking: int = None
    winStreakBonusRateList: List[PvpWinStreakBonusRate] = None
    rewardItemMstId: int = None
    shopSeriesMstId: int = None
class TalismanTalismanRarityRecord(BaseModel):
    rarity: int = None
    gold: int = None
    levelUpCostGold: int = None
class TalismanTalismanConfig(BaseModel):
    talismanNumLimit: int = None
    rarityInfo: List[TalismanTalismanRarityRecord] = None
    maxSellNum: int = None
    useLevelUpTalismanNum: int = None
class MissionMissionConfig(BaseModel):
    beginnerMissionFirstMissionTitleMstId: int = None
    subscriptionMissionDoubleTermRewardScale: int = None
class GuildMinMaxInfo(BaseModel):
    min: int = None
    max: int = None
class GuildValidatorInfo(BaseModel):
    length: GuildMinMaxInfo = None
class GuildGuildValidator(BaseModel):
    guildName: GuildValidatorInfo = None
    guildDescription: GuildValidatorInfo = None
    guildNameOrId: GuildValidatorInfo = None
class GuildGuildConfig(BaseModel):
    maxGuildMemberNum: int = None
    guildRoleMstIdOfMember: int = None
    guildRoleMstIdOfGuildMaster: int = None
    guildRoleMstIdOfGuildSubMaster: int = None
    maxGuildSubMasterNum: int = None
    masterMigrateNotLoginDay: int = None
    maxJoinRequestNum: int = None
    maxReceiveJoinRequestNum: int = None
    maxScoutNum: int = None
    maxReceiveScoutNum: int = None
    validator: GuildGuildValidator = None
class GveMedalData(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    num: int = None
class GveGveConfig(BaseModel):
    dayPlayCount: int = None
    chainInitialLevel: int = None
    chainMaxLevel: int = None
    damageApiInterval: int = None
    participationMedal: GveMedalData = None
class PresentPresentBoxConfig(BaseModel):
    defaultExpireTime: str = None
class UserUserConfig(BaseModel):
    staminaRecoverSec: int = None
    maxStamina: int = None
    staminaUpperLimit: int = None
    staminaRecoverMaxCountInDay: int = None
    staminaRecoverGemInfoGemNum: int = None
    staminaRecoverGemInfoRecoverAmount: int = None
    staminaRecoverGemInfoMaxCountInDay: int = None
    restrictSetNameDays: int = None
    maxUserNameLength: int = None
    playerIdDigitNum: int = None
    defaultUserTitleMstId: int = None
    storeReviewMinPendingDays: int = None
    userExpMax: int = None
    maxCommentLength: int = None
class QuestOutGameDropNumSubscriptionRateInfo(BaseModel):
    regular: int = None
    premium: int = None
class QuestOutGameDropNumRateInfo(BaseModel):
    subscription: QuestOutGameDropNumSubscriptionRateInfo = None
class QuestOutGameQuestConfig(BaseModel):
    backGroundPlayAddLapTimeSeconds: int = None
    characterHeartDailyBattleClearLimit: int = None
    dropNumUpRate: QuestOutGameDropNumRateInfo = None
class TutorialTutorialStepRecord(BaseModel):
    name: str = None
    value: int = None
class TutorialTutorialBattleFixedAllyInfo(BaseModel):
    questStageMstId: int = None
    styleMstId: int = None
    styleMstIds: List[int] = None
class TutorialUnlockConditionTxtInfo(BaseModel):
    miniTutorialNumber: int = None
    unlockConditionTxt: str = None
class TutorialReleaseStageTalkConfig(BaseModel):
    releaseStageName: str = None
    releaseFlag: int = None
    releaseTalkFlag: int = None
    talkId: int = None
class TutorialTutorialConfig(BaseModel):
    tutorialStepList: List[TutorialTutorialStepRecord] = None
    finishTutorialStep: int = None
    tutorialBattleFixedAllyInfoList: List[TutorialTutorialBattleFixedAllyInfo] = None
    unlockConditionTxtInfoList: List[TutorialUnlockConditionTxtInfo] = None
    releaseStageTalkConfigList: List[TutorialReleaseStageTalkConfig] = None
    dungeonMstList: List[str] = None
    battleMstList: List[str] = None
class TowerfloorSkipConfig(BaseModel):
    prevFloor: int = None
    newFloor: int = None
class TowerTowerConfig(BaseModel):
    resetTowerSkipNum: int = None
    maxTowerSkipNumForItem: int = None
    maxSkipNumForItemRecoveryInADay: int = None
    saveFloor: List[int] = None
    floorSkip: List[TowerfloorSkipConfig] = None
class PartyFixParamsPowerRate(BaseModel):
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
    speed: int = None
class PartyRoleCoefficientInfo(BaseModel):
    role: int = None
    hp: int = None
    atk: int = None
    _def: int = Field(alias='def')
class PartyRateParamsPowerRate(BaseModel):
    criticalRate: int = None
    criticalDamageRate: int = None
    breakDamageRate: int = None
    healRate: int = None
    recoveryEpRate: int = None
    effectHitRate: int = None
    effectParryRate: int = None
class PartySkillCoefficientPerLevel(BaseModel):
    skillLevel: int = None
    coefficient: int = None
class PartySkillPowerRateInfo(BaseModel):
    baseConst: float = None
    exponent: float = None
    addConst: int = None
    coefficientPerLevel: List[PartySkillCoefficientPerLevel] = None
class PartyPowerRate(BaseModel):
    fixParams: PartyFixParamsPowerRate = None
    roleCoefficientInfoList: List[PartyRoleCoefficientInfo] = None
    skillPowerBaseValue: int = None
    specialAttackCoefficient: int = None
    skillCoefficient: int = None
    passiveSkillCoefficient: int = None
    normalAttackCoefficient: int = None
    rateParams: PartyRateParamsPowerRate = None
    specialAttack: PartySkillPowerRateInfo = None
    skill: PartySkillPowerRateInfo = None
    passiveSkill: PartySkillPowerRateInfo = None
    normalAttack: PartySkillPowerRateInfo = None
class PartySubStyleDataParamRate(BaseModel):
    slot: int = None
    achievedLevel: int = None
    rate: int = None
class PartyPartyConfig(BaseModel):
    partyNumMax: int = None
    nameLengthMax: int = None
    defaultSoloPartyName: str = None
    defaultBattlePartyName: str = None
    powerRate: PartyPowerRate = None
    subStyleDataParamRate: int = None
    subStyleDataParamRateInfo: List[PartySubStyleDataParamRate] = None
class ShopServiceInfo(BaseModel):
    label: str = None
    firstFree: bool = None
    rewardDetailAnnounceMstId: int = None
    resourceName: str = None
    titleDescription: str = None
    description: List[str] = None
    notesIos: List[str] = None
    notesAndroid: List[str] = None
class ShopSubscriptionConfig(BaseModel):
    subscriptionLabelList: List[str] = None
    serviceList: List[ShopServiceInfo] = None
class StoryEventStoryEventConfig(BaseModel):
    keyItemMstId: int = None
    keyItemNum: int = None
    archiveEventItemId: int = None
    maxPlayCountPerDay: int = None
    maxPlayCountPerDayArchive: int = None
    playCountRecoverGemInfoGemNum: int = None
    playCountRecoverGemInfoRecoverAmount: int = None
    playCountRecoverGemInfoMaxCountInDay: int = None
    playCountRecoverGemInfoMaxCount: int = None
class ChatChatConfig(BaseModel):
    directChatRoomListLimit: int = None
    groupChatRoomListLimit: int = None
    groupChatRoomCreationLimit: int = None
    groupChatRoomMemberLimit: int = None
    chatBlockUserLimit: int = None
    chatsExpireDays: int = None
class ConfigFirestoreConfig(BaseModel):
    firestoreCollectionPath: str = None
class TermsTermsConfig(BaseModel):
    latestTermNumChat: int = None
    termsUpdatedTextChat: List[TermsTermsInfo] = None
class GatheringGatheringShortcutAmountRecord(BaseModel):
    times: int = None
    amount: int = None
class GatheringGatheringShortcutCountConfig(BaseModel):
    incAmount: List[GatheringGatheringShortcutAmountRecord] = None
class GatheringGatheringConfig(BaseModel):
    gatheringMaxHours: int = None
    gatheringShortcutHours: int = None
    perMinutes: int = None
    gatheringShortcutCount: GatheringGatheringShortcutCountConfig = None
class GvgGvgConfig(BaseModel):
    preLeagueMatchDayList: List[int] = None
class ScoreAttackScoreAttackConfig(BaseModel):
    topRankingViewNumber: int = None
    outOfRankingViewNumber: int = None
class ConfigAppResourceConfig(BaseModel):
    allowedBgmList: List[str] = None
    allowedStreamingMovieList: List[str] = None
    replaceStreamingMovieList: List[str] = None
    forEnglishStreamingMovieList: List[str] = None
class ConfigPurgeDataRecord(BaseModel):
    id: int = None
    purgeType: int = None
    target: int = None
    pathList: List[str] = None
class ConfigPurgeConfig(BaseModel):
    purgeDataList: List[ConfigPurgeDataRecord] = None
class SelectionAbilityMainSelectionAbilityRarityInfo(BaseModel):
    rarity: int = None
    maxSubSelectionAbilityNum: int = None
    gainSubSelectionAbilityItemNum: int = None
class SelectionAbilitySubSelectionAbilityRarityInfo(BaseModel):
    rarity: int = None
    gainSubSelectionAbilityItemNum: int = None
class SelectionAbilityEnableMainSelectionAbilityInfo(BaseModel):
    selectionAbilityNum: int = None
    itemNum: int = None
class SelectionAbilitySelectionAbilityConfig(BaseModel):
    enableMainSelectionAbilityItemMstId: int = None
    enableMainSelectionAbilityItemNum: int = None
    lockSubSelectionAbilityItemMstId: int = None
    lockSubSelectionAbilityItemNum: int = None
    learnSubSelectionAbilityItemMstId: int = None
    learnSubSelectionAbilityItemNum: int = None
    learnSubSelectionAbilityGoldNum: int = None
    maxMainSelectionAbilityNum: int = None
    maxStockSelectionAbilityNum: int = None
    mainRarityInfoList: List[SelectionAbilityMainSelectionAbilityRarityInfo] = None
    subRarityInfoList: List[SelectionAbilitySubSelectionAbilityRarityInfo] = None
    enableMainSelectionAbility: List[SelectionAbilityEnableMainSelectionAbilityInfo] = None
    useItemMaxForLearnSelectionAbility: int = None
    learnMainExAbilityItemMstId: int = None
    learnMainAbilityValidDateTime: str = None
class MultiRaidMultiRaidConfig(BaseModel):
    maxJoinRoomCount: int = None
    maxJoinUserCount: int = None
    battleTimeLimitSec: int = None
    maxStamina: int = None
    superiorItemMstId: int = None
    inferiorItemMstId: int = None
    maxPlayCountPerDay: int = None
    staminaRecoverSec: int = None
    staminaRecoverNum: int = None
    staminaUpperLimit: int = None
    staminaMaxCountInDay: int = None
    resultDisplayLimitDays: int = None
    battleClearNumForDailyBonusReward: int = None
    scoreCalcConstant: int = None
    callAddDamageSec: int = None
    callSyncBattleInfoSec: int = None
class CollectionCollectionIllustAchieveDataRecord(BaseModel):
    userId: int = None
    collectionIllustMstId: int = None
    achievedConditionGroupIdCsv1: str = None
    achievedConditionGroupIdCsv2: str = None
    completeProgressConditionGroupIdCsv: str = None
class CollectionMagiaRecordCharacterMstRecord(BaseModel):
    magiaRecordCharacterMstId: int = None
    name: str = None
    resourceName: str = None
class CollectionMagiaRecordMemoriaMstRecord(BaseModel):
    magiaRecordMemoriaMstId: int = None
    name: str = None
    resourceName: str = None
class ChatChatRoomInfo(BaseModel):
    roomType: int = None
    roomDocumentId: str = None
    roomName: str = None
class CharacterCharacterHeartLevelUpInfo(BaseModel):
    characterMstId: int = None
    beforeHeartLevel: int = None
    beforeHeartExp: int = None
    afterHeartLevel: int = None
    afterHeartExp: int = None
class QuestBattleAcquiredQuestBonusRewardInfo(BaseModel):
    objectReceiveType: int = None
    objectId: int = None
    addNum: int = None
class SelectionAbilityAcquiredSelectionAbilityInfo(BaseModel):
    styleMstId: int = None
    selectionAbilityMstId: int = None
class ExplorationDungeonResult(BaseModel):
    fieldStageUserData: ExplorationFieldStageUserDataRecord = None
    acquiredQuestRewardMstIds: List[int] = None
    achievedConditionGroupIds: List[int] = None
    fieldStageCollectionInfo: CollectionFieldStageCollectionInfo = None
    clearedDungeonEventMstIds: List[int] = None
class ExplorationBattleExplorationBattleResult(BaseModel):
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
    keyItemDataList: List[ItemItemDataRecord] = None
    characterLevelUpInfoList: List[CharacterCharacterLevelUpInfo] = None
    styleLevelUpInfoList: List[StyleStyleLevelUpInfo] = None
    achievedConditionGroupIds: List[int] = None
    fieldStageCollectionInfo: CollectionFieldStageCollectionInfo = None
    featureReleaseList: List[TutorialFeatureRelease] = None
    nextBattleQuestStageMstId: int = None
    nextBattleFieldPointMstId: int = None
    isFirstClear: bool = None
    isStoreReview: bool = None
    acquiredRewardMoney: int = None
    isUserExpStoredMessage: bool = None
class ExplorationQuestMapEffectedInfo(BaseModel):
    questMapMstId: int = None
    difficulty: int = None
