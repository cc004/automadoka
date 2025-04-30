from typing import List, Dict
from .modelbase import RequestBase, MstRequestBase
from .responses import *
from .common import *
from .enums import *
from pydantic import Field

class WebPlayApiLoginLogRequest(RequestBase[WebPlayApiLoginLogResponse]):
    sessionToken: str = None
    @property
    def url(self) -> str:
        return "/api/web_play/login_log"
class WebPlayApiGetUserMigrationInfoRequest(RequestBase[WebPlayApiGetUserMigrationInfoResponse]):
    sessionToken: str = None
    @property
    def url(self) -> str:
        return "/api/web_play/get_user_migration_info"
class WebPayApiPurchaseRequest(RequestBase[WebPayApiPurchaseResponse]):
    productId: str = None
    @property
    def url(self) -> str:
        return "/api/web_pay/purchase"
class WebPayApiGetPurchaseResultRequest(RequestBase[WebPayApiGetPurchaseResultResponse]):
    purchaseId: str = None
    @property
    def url(self) -> str:
        return "/api/web_pay/get_purchase_result"
class WebPayApiRestoreRequest(RequestBase[WebPayApiRestoreResponse]):
    @property
    def url(self) -> str:
        return "/api/web_pay/restore"
class WebPayApiCancelLatestRequest(RequestBase[WebPayApiCancelLatestResponse]):
    @property
    def url(self) -> str:
        return "/api/web_pay/cancel_latest"
class TitleApiGetTitleTopDataRequest(RequestBase[TitleApiGetTitleTopDataResponse]):
    osType: int = None
    storeType: int = None
    appVersion: str = None
    @property
    def url(self) -> str:
        return "/api/title/get_title_top_data"
class TermsApiGetUpdatedTermsRequest(RequestBase[TermsApiGetUpdatedTermsResponse]):
    storeType: int = None
    @property
    def url(self) -> str:
        return "/api/terms/get_updated_terms"
class TermsApiAgreeLatestTermsRequest(RequestBase[TermsApiAgreeLatestTermsResponse]):
    storeType: int = None
    agreeTermId: int = None
    @property
    def url(self) -> str:
        return "/api/terms/agree_latest_terms"
class TermsApiAgreeChatTermsRequest(RequestBase[TermsApiAgreeChatTermsResponse]):
    @property
    def url(self) -> str:
        return "/api/terms/agree_chat_terms"
class TalismanApiGetTalismanListRequest(RequestBase[TalismanApiGetTalismanListResponse]):
    @property
    def url(self) -> str:
        return "/api/talisman/get_talisman_list"
class TalismanApiTalismanLevelUpRequest(RequestBase[TalismanApiTalismanLevelUpResponse]):
    talismanDataId: int = None
    consumeTalismanDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/talisman/talisman_level_up"
class TalismanApiTalismanSellRequest(RequestBase[TalismanApiTalismanSellResponse]):
    talismanDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/talisman/talisman_sell"
class TalismanApiSetTalismanProtectRequest(RequestBase[TalismanApiSetTalismanProtectResponse]):
    talismanDataId: int = None
    isProtect: bool = None
    @property
    def url(self) -> str:
        return "/api/talisman/set_talisman_protect"
class ServerApiGetTimeZoneInfoRequest(RequestBase[ServerApiGetTimeZoneInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/server/get_time_zone_info"
class ServerApiCertHashListRequest(RequestBase[ServerApiCertHashListResponse]):
    @property
    def url(self) -> str:
        return "/api/server/cert_hash_list"
class SerialCampaignApiInputSerialCodeRequest(RequestBase[SerialCampaignApiInputSerialCodeResponse]):
    serialCode: str = None
    @property
    def url(self) -> str:
        return "/api/serial_campaign/input_serial_code"
class SerialCampaignApiPreAppLinkRequest(RequestBase[SerialCampaignApiPreAppLinkResponse]):
    serialCode: str = None
    @property
    def url(self) -> str:
        return "/api/serial_campaign/pre_app_link"
class SampleApiHttpConnectRequest(RequestBase[SampleApiHttpConnectResponse]):
    @property
    def url(self) -> str:
        return "/api/sample/http_connect"
class NotificationApiRegisterRequest(RequestBase[NotificationApiRegisterResponse]):
    deviceToken: str = None
    @property
    def url(self) -> str:
        return "/api/notification/register"
class NotificationApiSetOsRequest(RequestBase[NotificationApiSetOsResponse]):
    os: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_os"
class NotificationApiSetLanguageRequest(RequestBase[NotificationApiSetLanguageResponse]):
    language: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_language"
class NotificationApiSetRegionRequest(RequestBase[NotificationApiSetRegionResponse]):
    region: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_region"
class NotificationApiSetTimezoneRequest(RequestBase[NotificationApiSetTimezoneResponse]):
    timezone: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_timezone"
class NotificationApiUnsetOsRequest(RequestBase[NotificationApiUnsetOsResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_os"
class NotificationApiUnsetRegionRequest(RequestBase[NotificationApiUnsetRegionResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_region"
class NotificationApiUnsetLanguageRequest(RequestBase[NotificationApiUnsetLanguageResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_language"
class NotificationApiUnsetTimezoneRequest(RequestBase[NotificationApiUnsetTimezoneResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_timezone"
class NotificationApiSetTagRequest(RequestBase[NotificationApiSetTagResponse]):
    tag: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_tag"
class NotificationApiUnsetTagRequest(RequestBase[NotificationApiUnsetTagResponse]):
    tag: str = None
    @property
    def url(self) -> str:
        return "/api/notification/unset_tag"
class MstApiGetItemMstListRequest(MstRequestBase[ItemItemMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_item_mst_list"
class MstApiGetCardMstListRequest(MstRequestBase[CardCardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_card_mst_list"
class MstApiGetCardLimitBreakMstListRequest(MstRequestBase[CardCardLimitBreakMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_card_limit_break_mst_list"
class MstApiGetSkillMstListRequest(MstRequestBase[SkillSkillMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_mst_list"
class MstApiGetSkillLevelUpConditionMstListRequest(MstRequestBase[SkillSkillLevelUpConditionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_level_up_condition_mst_list"
class MstApiGetCharacterAwakeMstListRequest(MstRequestBase[CharacterCharacterAwakeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_awake_mst_list"
class MstApiGetCharacterMstListRequest(MstRequestBase[CharacterCharacterMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_mst_list"
class MstApiGetCharacterProfileMstListRequest(MstRequestBase[CharacterCharacterProfileMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_profile_mst_list"
class MstApiGetCharacterHeartMstListRequest(MstRequestBase[CharacterCharacterHeartMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_mst_list"
class MstApiGetCharacterHeartParamUpGroupMstListRequest(MstRequestBase[CharacterCharacterHeartParamUpGroupMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_param_up_group_mst_list"
class MstApiGetCharacterHeartObjectRewardMstListRequest(MstRequestBase[CharacterCharacterHeartObjectRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_object_reward_mst_list"
class MstApiGetCharacterHeartLevelUpMstListRequest(MstRequestBase[CharacterCharacterHeartLevelUpMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_level_up_mst_list"
class MstApiGetCharacterTeamMstListRequest(MstRequestBase[CharacterCharacterTeamMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_team_mst_list"
class MstApiGetStyleMstListRequest(MstRequestBase[StyleStyleMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_mst_list"
class MstApiGetTowerMstListRequest(MstRequestBase[TowerTowerMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_tower_mst_list"
class MstApiGetQuestCategoryMstListRequest(MstRequestBase[QuestOutGameQuestCategoryMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_category_mst_list"
class MstApiGetQuestMapMstListRequest(MstRequestBase[QuestOutGameQuestMapMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_map_mst_list"
class MstApiGetQuestGroupMstListRequest(MstRequestBase[QuestOutGameQuestGroupMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_group_mst_list"
class MstApiGetQuestStageMstListRequest(MstRequestBase[QuestOutGameQuestStageMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_stage_mst_list"
class MstApiGetQuestConditionMstListRequest(MstRequestBase[QuestOutGameQuestConditionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_condition_mst_list"
class MstApiGetMissionTitleMstListRequest(MstRequestBase[MissionMissionTitleMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_title_mst_list"
class MstApiGetMissionTransitionMstListRequest(MstRequestBase[MissionMissionTransitionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_transition_mst_list"
class MstApiGetSubscriptionMissionRewardMstListRequest(MstRequestBase[MissionSubscriptionMissionRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_subscription_mission_reward_mst_list"
class MstApiGetMissionMstListRequest(MstRequestBase[MissionMissionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_mst_list"
class MstApiGetEnemyMstListRequest(MstRequestBase[QuestOutGameEnemyMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_mst_list"
class MstApiGetEnemyProfileMstListRequest(MstRequestBase[QuestOutGameEnemyProfileMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_profile_mst_list"
class MstApiGetQuestEnemyAppearanceMstListRequest(MstRequestBase[QuestOutGameQuestEnemyAppearanceMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_enemy_appearance_mst_list"
class MstApiGetQuestEnemySkillSetMstListRequest(MstRequestBase[QuestOutGameQuestEnemySkillSetMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_enemy_skill_set_mst_list"
class MstApiGetBreakMstListRequest(MstRequestBase[QuestOutGameBreakMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_break_mst_list"
class MstApiGetAbilityEffectTypeMstListRequest(MstRequestBase[SkillAbilityEffectTypeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_ability_effect_type_mst_list"
class MstApiGetSkillDetailMstListRequest(MstRequestBase[SkillSkillDetailMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_detail_mst_list"
class MstApiGetQuestRewardMstListRequest(MstRequestBase[QuestOutGameQuestRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_reward_mst_list"
class MstApiGetFieldSeriesMstListRequest(MstRequestBase[ExplorationFieldSeriesMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_series_mst_list"
class MstApiGetFieldStageMstListRequest(MstRequestBase[ExplorationFieldStageMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_stage_mst_list"
class MstApiGetAdvMstListRequest(MstRequestBase[ExplorationAdvMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_adv_mst_list"
class MstApiGetAdvTitleMstListRequest(MstRequestBase[ExplorationAdvTitleMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_adv_title_mst_list"
class MstApiGetObjectReceiveTypeMstListRequest(MstRequestBase[ObjectObjectReceiveTypeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_object_receive_type_mst_list"
class MstApiGetPayTypeMstListRequest(MstRequestBase[ObjectPayTypeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pay_type_mst_list"
class MstApiGetTalismanMstListRequest(MstRequestBase[TalismanTalismanMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_mst_list"
class MstApiGetTalismanParamMstListRequest(MstRequestBase[TalismanTalismanParamMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_param_mst_list"
class MstApiGetTalismanParamEffectMstListRequest(MstRequestBase[TalismanTalismanParamEffectMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_param_effect_mst_list"
class MstApiGetTalismanSeriesMstListRequest(MstRequestBase[TalismanTalismanSeriesMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_series_mst_list"
class MstApiGetPassiveSkillMstListRequest(MstRequestBase[SkillPassiveSkillMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_passive_skill_mst_list"
class MstApiGetPassiveSkillDetailMstListRequest(MstRequestBase[SkillPassiveSkillDetailMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_passive_skill_detail_mst_list"
class MstApiGetLeaderSkillMstListRequest(MstRequestBase[SkillLeaderSkillMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_leader_skill_mst_list"
class MstApiGetLeaderSkillDetailMstListRequest(MstRequestBase[SkillLeaderSkillDetailMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_leader_skill_detail_mst_list"
class MstApiGetPvpRankingRewardMstListRequest(MstRequestBase[PvpPvpRankingRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pvp_ranking_reward_mst_list"
class MstApiGetPvpPointRewardMstListRequest(MstRequestBase[PvpPvpPointRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pvp_point_reward_mst_list"
class MstApiGetUserTitleMstListRequest(MstRequestBase[UserTitleUserTitleMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_user_title_mst_list"
class MstApiGetGuildTitleMstListRequest(MstRequestBase[GuildGuildTitleMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_title_mst_list"
class MstApiGetUserLevelUpMstListRequest(MstRequestBase[UserUserLevelUpMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_user_level_up_mst_list"
class MstApiGetShopSeriesMstListRequest(MstRequestBase[ShopShopSeriesMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_series_mst_list"
class MstApiGetShopMstListRequest(MstRequestBase[ShopShopMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_mst_list"
class MstApiGetShopDetailMstListRequest(MstRequestBase[ShopShopDetailMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_detail_mst_list"
class MstApiGetBannerMstListRequest(MstRequestBase[HomeBannerMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_banner_mst_list"
class MstApiGetBannerLabelMstListRequest(MstRequestBase[HomeBannerLabelMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_banner_label_mst_list"
class MstApiGetHomeBannerMstListRequest(MstRequestBase[HomeHomeBannerMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_home_banner_mst_list"
class MstApiGetHomeAppealMstListRequest(MstRequestBase[HomeHomeAppealMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_home_appeal_mst_list"
class MstApiGetTipsMstListRequest(MstRequestBase[TipsTipsMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_tips_mst_list"
class MstApiGetGveMstListRequest(MstRequestBase[GveGveMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_mst_list"
class MstApiGetGveStageMstListRequest(MstRequestBase[GveGveStageMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_stage_mst_list"
class MstApiGetGveStageRewardMstListRequest(MstRequestBase[GveGveStageRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_stage_reward_mst_list"
class MstApiGetMapGveMstListRequest(MstRequestBase[MapGveMapGveMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_mst_list"
class MstApiGetMapGveAreaMstListRequest(MstRequestBase[MapGveMapGveAreaMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_area_mst_list"
class MstApiGetMapGvePointMstListRequest(MstRequestBase[MapGveMapGvePointMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_point_mst_list"
class MstApiGetLoginBonusMstListRequest(MstRequestBase[LoginBonusLoginBonusMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_login_bonus_mst_list"
class MstApiGetLoginBonusRewardMstListRequest(MstRequestBase[LoginBonusLoginBonusRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_login_bonus_reward_mst_list"
class MstApiGetStyleFigureMstListRequest(MstRequestBase[StyleStyleFigureMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_figure_mst_list"
class MstApiGetStyleFigureStoryMstListRequest(MstRequestBase[StyleStyleFigureStoryMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_figure_story_mst_list"
class MstApiGetStyleParamUpTreeMstListRequest(MstRequestBase[StyleStyleParamUpTreeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_tree_mst_list"
class MstApiGetStyleParamUpMstListRequest(MstRequestBase[StyleStyleParamUpMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_mst_list"
class MstApiGetStyleParamUpCostMstListRequest(MstRequestBase[StyleStyleParamUpCostMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_cost_mst_list"
class MstApiGetStyleParamUpEffectMstListRequest(MstRequestBase[StyleStyleParamUpEffectMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_effect_mst_list"
class MstApiGetStyleLimitBreakMstListRequest(MstRequestBase[StyleStyleLimitBreakMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_limit_break_mst_list"
class MstApiGetStyleLimitBreakEffectMstListRequest(MstRequestBase[StyleStyleLimitBreakEffectMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_limit_break_effect_mst_list"
class MstApiGetStyleLevelUpMstListRequest(MstRequestBase[StyleStyleLevelUpMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_level_up_mst_list"
class MstApiGetStyleVoiceMstListRequest(MstRequestBase[StyleStyleVoiceMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_voice_mst_list"
class MstApiGetGvgPointRewardMstListRequest(MstRequestBase[GvgGvgPointRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_point_reward_mst_list"
class MstApiGetGvgRankingRewardMstListRequest(MstRequestBase[GvgGvgRankingRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_ranking_reward_mst_list"
class MstApiGetChatStampMstListRequest(MstRequestBase[ChatChatStampMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_chat_stamp_mst_list"
class MstApiGetBattleConditionMstListRequest(MstRequestBase[QuestBattleBattleConditionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_battle_condition_mst_list"
class MstApiGetBattleConditionSetMstListRequest(MstRequestBase[QuestBattleBattleConditionSetMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_battle_condition_set_mst_list"
class MstApiGetEnemyConditionSetsAndActionMstListRequest(MstRequestBase[QuestBattleEnemyConditionSetsAndActionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_condition_sets_and_action_mst_list"
class MstApiGetDioramaBackgroundMstListRequest(MstRequestBase[CollectionDioramaBackgroundMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_diorama_background_mst_list"
class MstApiGetLive2DParamMstListRequest(MstRequestBase[CollectionLive2DParamMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_live2_d_param_mst_list"
class MstApiGetGvgMstListRequest(MstRequestBase[GvgGvgMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_mst_list"
class MstApiGetSoundMstListRequest(MstRequestBase[SoundSoundMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_sound_mst_list"
class MstApiGetCollectionIllustMstListRequest(MstRequestBase[CollectionCollectionIllustMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_illust_mst_list"
class MstApiGetCollectionIllustPieceMstListRequest(MstRequestBase[CollectionCollectionIllustPieceMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_illust_piece_mst_list"
class MstApiGetCollectionParamUpMstListRequest(MstRequestBase[CollectionCollectionParamUpMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_mst_list"
class MstApiGetCollectionParamUpLevelMstListRequest(MstRequestBase[CollectionCollectionParamUpLevelMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_level_mst_list"
class MstApiGetCollectionParamUpEffectMstListRequest(MstRequestBase[CollectionCollectionParamUpEffectMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_effect_mst_list"
class MstApiGetCollectionConditionGroupMstListRequest(MstRequestBase[CollectionCollectionConditionGroupMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_condition_group_mst_list"
class MstApiGetCollectionConditionMstListRequest(MstRequestBase[CollectionCollectionConditionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_condition_mst_list"
class MstApiGetCollectionRewardMstListRequest(MstRequestBase[CollectionCollectionRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_reward_mst_list"
class MstApiGetStoryEventMstListRequest(MstRequestBase[StoryEventStoryEventMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_mst_list"
class MstApiGetStoryEventQuestStageMstListRequest(MstRequestBase[StoryEventStoryEventQuestStageMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_quest_stage_mst_list"
class MstApiGetMiniTutorialMstListRequest(MstRequestBase[TutorialMiniTutorialMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mini_tutorial_mst_list"
class MstApiGetStoryEventScenarioMstListRequest(MstRequestBase[StoryEventStoryEventScenarioMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_scenario_mst_list"
class MstApiGetStoryEventScenarioRewardMstListRequest(MstRequestBase[StoryEventStoryEventScenarioRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_scenario_reward_mst_list"
class MstApiGetStoryEventBonusRateMstListRequest(MstRequestBase[StoryEventStoryEventBonusRateMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_bonus_rate_mst_list"
class MstApiGetDungeonMstListRequest(MstRequestBase[DungeonDungeonMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_mst_list"
class MstApiGetDungeonTypeMstListRequest(MstRequestBase[DungeonDungeonTypeMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_type_mst_list"
class MstApiGetDungeonRoomMstListRequest(MstRequestBase[DungeonDungeonRoomMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_room_mst_list"
class MstApiGetDungeonEventMstListRequest(MstRequestBase[DungeonDungeonEventMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_event_mst_list"
class MstApiGetFieldStratumMstListRequest(MstRequestBase[ExplorationFieldStratumMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_stratum_mst_list"
class MstApiGetFieldPointMstListRequest(MstRequestBase[ExplorationFieldPointMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_point_mst_list"
class MstApiGetBossDirectionMstListRequest(MstRequestBase[ExplorationBossDirectionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_boss_direction_mst_list"
class MstApiGetGatheringLevelMstListRequest(MstRequestBase[GatheringGatheringLevelMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gathering_level_mst_list"
class MstApiGetGatheringRewardMstListRequest(MstRequestBase[GatheringGatheringRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gathering_reward_mst_list"
class MstApiGetScoreAttackMstListRequest(MstRequestBase[ScoreAttackScoreAttackMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_mst_list"
class MstApiGetScoreAttackStageMstListRequest(MstRequestBase[ScoreAttackScoreAttackStageMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_stage_mst_list"
class MstApiGetScoreAttackHighScoreRewardMstListRequest(MstRequestBase[ScoreAttackScoreAttackHighScoreRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_high_score_reward_mst_list"
class MstApiGetScoreAttackTotalScoreRewardMstListRequest(MstRequestBase[ScoreAttackScoreAttackTotalScoreRewardMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_total_score_reward_mst_list"
class MstApiGetCalculationPointPolicyMstListRequest(MstRequestBase[CalcPointCalculationPointPolicyMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_calculation_point_policy_mst_list"
class MstApiGetGuildMissionMstListRequest(MstRequestBase[GuildMissionGuildMissionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_mission_mst_list"
class MstApiGetGuildMissionTransitionMstListRequest(MstRequestBase[GuildMissionGuildMissionTransitionMstRecord]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_mission_transition_mst_list"
class MapGveApiGetTopInfoRequest(RequestBase[MapGveApiGetTopInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/map_gve/get_top_info"
class MapGveApiReachPointRequest(RequestBase[MapGveApiReachPointResponse]):
    mapGvePointMstId: int = None
    @property
    def url(self) -> str:
        return "/api/map_gve/reach_point"
class LoginApiLoginRequest(RequestBase[LoginApiLoginResponse]):
    appVersion: str = None
    urlParam: str = None
    deviceModel: str = None
    osType: int = None
    osVersion: str = None
    storeType: int = None
    graphicsDeviceId: int = None
    graphicsDeviceVendorId: int = None
    processorCount: int = None
    processorType: str = None
    supportedRenderTargetCount: int = None
    supports3DTextures: bool = None
    supportsAccelerometer: bool = None
    supportsComputeShaders: bool = None
    supportsGyroscope: bool = None
    supportsImageEffects: bool = None
    supportsInstancing: bool = None
    supportsLocationService: bool = None
    supportsRenderTextures: bool = None
    supportsRenderToCubemap: bool = None
    supportsShadows: bool = None
    supportsSparseTextures: bool = None
    supportsStencil: int = None
    supportsVibration: bool = None
    uuid: str = None
    xuid: int = None
    @property
    def url(self) -> str:
        return "/api/login"
class InAppSnsApiCreateLoginUrlRequest(RequestBase[InAppSnsApiCreateLoginUrlResponse]):
    platform: int = None
    @property
    def url(self) -> str:
        return "/api/in_app_sns/create_login_url"
class InAppSnsApiGetAccessTokenRequest(RequestBase[InAppSnsApiGetAccessTokenResponse]):
    state: str = None
    @property
    def url(self) -> str:
        return "/api/in_app_sns/get_access_token"
class HariboteChatApiGetMessageDataListRequest(RequestBase[HariboteChatApiGetMessageDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/haribote_chat/get_message_data_list"
class HariboteChatApiSendMessageRequest(RequestBase[HariboteChatApiSendMessageResponse]):
    message: str = None
    @property
    def url(self) -> str:
        return "/api/debug/haribote_chat/send_message"
class FirestoreApiCreateTokenRequest(RequestBase[FirestoreApiCreateTokenResponse]):
    @property
    def url(self) -> str:
        return "/api/firestore/create_token"
class ExplorationBattleApiInitializeStageV4Request(RequestBase[ExplorationBattleApiInitializeStageV4Response]):
    fieldStageMstId: int = None
    fieldPointMstId: int = None
    dungeonEventMstId: int = None
    dungeonRoomMstId: int = None
    bossDirectionMstId: int = None
    presetEventIndex: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/initialize_stage_v4"
class ExplorationBattleApiFinalizeStageForUserV4Request(RequestBase[ExplorationBattleApiFinalizeStageForUserV4Response]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/finalize_stage_for_user_v4"
class ExplorationBattleApiGetExplorationInfoRequest(RequestBase[ExplorationBattleApiGetExplorationInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/get_exploration_info"
class ExplorationBattleApiRetireRequest(RequestBase[ExplorationBattleApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/retire"
class DebugUserApiRecoverStaminaRequest(RequestBase[DebugUserApiRecoverStaminaResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_user/recover_stamina"
class DebugSubscriptionApiIsValidSubscriptionRequest(RequestBase[DebugSubscriptionApiIsValidSubscriptionResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_subscription/is_valid_subscription"
class DebugSubscriptionApiDoSubscribeForceRequest(RequestBase[DebugSubscriptionApiDoSubscribeForceResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_subscription/do_subscribe_force"
class ConfigApiGetConfigRequest(RequestBase[ConfigApiGetConfigResponse]):
    @property
    def url(self) -> str:
        return "/api/config/get_config"
class AppVersionApiGetReviewVersionDataRequest(RequestBase[AppVersionApiGetReviewVersionDataResponse]):
    storeType: int = None
    appVersion: str = None
    @property
    def url(self) -> str:
        return "/api/app_version/get_review_version_data"
class AkamaiApiCreateTokenRequest(RequestBase[AkamaiApiCreateTokenResponse]):
    @property
    def url(self) -> str:
        return "/api/akamai/create_token"
class TowerApiGetTowerTopRequest(RequestBase[TowerApiGetTowerTopResponse]):
    @property
    def url(self) -> str:
        return "/api/tower/get_tower_top"
class TowerApiRecoverySkipNumRequest(RequestBase[TowerApiRecoverySkipNumResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/tower/recovery_skip_num"
class TowerApiSkipQuestBattleRequest(RequestBase[TowerApiSkipQuestBattleResponse]):
    questStageMstId: int = None
    repeatNum: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/tower/skip_quest_battle"
class StyleApiGetStyleDataListRequest(RequestBase[StyleApiGetStyleDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/style/get_style_data_list"
class StyleApiStyleLevelUpRequest(RequestBase[StyleApiStyleLevelUpResponse]):
    styleMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/style/style_level_up"
class StyleApiStyleLevelUpVer2Request(RequestBase[StyleApiStyleLevelUpVer2Response]):
    styleMstId: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_level_up_ver2"
class StyleApiStyleSkillLevelUpRequest(RequestBase[StyleApiStyleSkillLevelUpResponse]):
    styleMstId: int = None
    skillLevelUpType: int = None
    skillNo: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_skill_level_up"
class StyleApiStyleSpecialAttackSkillLevelUpRequest(RequestBase[StyleApiStyleSpecialAttackSkillLevelUpResponse]):
    styleMstId: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_special_attack_skill_level_up"
class StyleApiStyleLimitBreakRequest(RequestBase[StyleApiStyleLimitBreakResponse]):
    styleMstId: int = None
    itemNum: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_limit_break"
class StyleApiOpenStyleParamUpTreeRequest(RequestBase[StyleApiOpenStyleParamUpTreeResponse]):
    styleMstId: int = None
    styleParamUpTreeMstId: int = None
    @property
    def url(self) -> str:
        return "/api/style/open_style_param_up_tree"
class StyleApiStyleParamUpRequest(RequestBase[StyleApiStyleParamUpResponse]):
    styleMstId: int = None
    styleParamUpTreeMstId: int = None
    paramUpType: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_param_up"
class StyleApiUpdateAlreadyViewRequest(RequestBase[StyleApiUpdateAlreadyViewResponse]):
    styleMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/style/update_already_view"
class StoryEventApiGetTopRequest(RequestBase[StoryEventApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/story_event/get_top"
class StoryEventApiGetArchiveEventListRequest(RequestBase[StoryEventApiGetArchiveEventListResponse]):
    @property
    def url(self) -> str:
        return "/api/story_event/get_archive_event_list"
class StoryEventApiOpenStoryRequest(RequestBase[StoryEventApiOpenStoryResponse]):
    storyEventMstId: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/open_story"
class StoryEventApiScenarioReadRequest(RequestBase[StoryEventApiScenarioReadResponse]):
    storyEventScenarioMstId: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/scenario_read"
class StoryEventApiRecoverPlayableCountRequest(RequestBase[StoryEventApiRecoverPlayableCountResponse]):
    storyEventMstId: int = None
    recoverCount: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/recover_playable_count"
class ShopApiGetShopListRequest(RequestBase[ShopApiGetShopListResponse]):
    @property
    def url(self) -> str:
        return "/api/shop/get_shop_list"
class ShopApiBuyRequest(RequestBase[ShopApiBuyResponse]):
    shopMstId: int = None
    shopSeriesMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/shop/buy"
class ShopApiGetShopPaymentMstListRequest(RequestBase[ShopApiGetShopPaymentMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/shop/get_shop_payment_mst_list"
class ScoreAttackApiGetScoreAttackTopRequest(RequestBase[ScoreAttackApiGetScoreAttackTopResponse]):
    scoreAttackMstId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_score_attack_top"
class ScoreAttackApiGetRankingInfoRequest(RequestBase[ScoreAttackApiGetRankingInfoResponse]):
    scoreAttackMstId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_ranking_info"
class ScoreAttackApiInitializeStageRequest(RequestBase[ScoreAttackApiInitializeStageResponse]):
    scoreAttackStageMstId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/initialize_stage"
class ScoreAttackApiGetScoreAttackInfoRequest(RequestBase[ScoreAttackApiGetScoreAttackInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_score_attack_info"
class ScoreAttackApiFinalizeStageForUserRequest(RequestBase[ScoreAttackApiFinalizeStageForUserResponse]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/finalize_stage_for_user"
class ScoreAttackApiRetireRequest(RequestBase[ScoreAttackApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/score_attack/retire"
class PvpApiGetPvpTopRequest(RequestBase[PvpApiGetPvpTopResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_pvp_top"
class PvpApiGetRankingInfoRequest(RequestBase[PvpApiGetRankingInfoResponse]):
    mode: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_ranking_info"
class PvpApiGetCandidateEnemyUserListRequest(RequestBase[PvpApiGetCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_candidate_enemy_user_list"
class PvpApiGetEnemyUserInfoRequest(RequestBase[PvpApiGetEnemyUserInfoResponse]):
    chooseEnemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_enemy_user_info"
class PvpApiInitializeStageRequest(RequestBase[PvpApiInitializeStageResponse]):
    chooseEnemyUserId: int = None
    partyDataId: int = None
    isConsumeGem: bool = None
    @property
    def url(self) -> str:
        return "/api/pvp/initialize_stage"
class PvpApiRetireRequest(RequestBase[PvpApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/pvp/retire"
class PvpApiGetPvpInfoRequest(RequestBase[PvpApiGetPvpInfoResponse]):
    roomId: str = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_pvp_info"
class PvpApiFinalizeStageRequest(RequestBase[PvpApiFinalizeStageResponse]):
    roomId: str = None
    winUserId: int = None
    result: int = None
    battleLog: str = None
    @property
    def url(self) -> str:
        return "/api/pvp/finalize_stage"
class PvpApiFinalizeStageForUserRequest(RequestBase[PvpApiFinalizeStageForUserResponse]):
    roomId: str = None
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/finalize_stage_for_user"
class PvpApiGetMatchHistoryRequest(RequestBase[PvpApiGetMatchHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_history"
class PvpApiGetMatchDetailHistoryRequest(RequestBase[PvpApiGetMatchDetailHistoryResponse]):
    pvpDataId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_detail_history"
class PvpApiGetMatchCharacterBuildDetailRequest(RequestBase[PvpApiGetMatchCharacterBuildDetailResponse]):
    pvpDataId: int = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_character_build_detail"
class PvpApiGetRankingUserCharacterBuildDetailRequest(RequestBase[PvpApiGetRankingUserCharacterBuildDetailResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_ranking_user_character_build_detail"
class UserTitleApiGetUserTitleDataListRequest(RequestBase[UserTitleApiGetUserTitleDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/user_title/get_user_title_data_list"
class UserApiGetUserDataRequest(RequestBase[UserApiGetUserDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_data"
class UserApiGetUserParamDataRequest(RequestBase[UserApiGetUserParamDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_param_data"
class UserApiGetInitDataListRequest(RequestBase[UserApiGetInitDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_init_data_list"
class UserApiGetUserProfileDataRequest(RequestBase[UserApiGetUserProfileDataResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_user_profile_data"
class UserApiGetOtherUserProfileDataRequest(RequestBase[UserApiGetOtherUserProfileDataResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_other_user_profile_data"
class UserApiSetNameRequest(RequestBase[UserApiSetNameResponse]):
    name: str = None
    @property
    def url(self) -> str:
        return "/api/user/set_name"
class UserApiSetCommentRequest(RequestBase[UserApiSetCommentResponse]):
    comment: str = None
    @property
    def url(self) -> str:
        return "/api/user/set_comment"
class UserApiSetFavoriteInfoRequest(RequestBase[UserApiSetFavoriteInfoResponse]):
    characterMstId: int = None
    styleMstId: int = None
    skillMstId: int = None
    @property
    def url(self) -> str:
        return "/api/user/set_favorite_info"
class UserApiSetDisplayUserTitleRequest(RequestBase[UserApiSetDisplayUserTitleResponse]):
    userTitleMstIds: List[int] = None
    value1List: List[int] = None
    @property
    def url(self) -> str:
        return "/api/user/set_display_user_title"
class UserApiSetStaminaRecoverRequest(RequestBase[UserApiSetStaminaRecoverResponse]):
    recoverType: int = None
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/user/set_stamina_recover"
class UserApiSaveOptionRequest(RequestBase[UserApiSaveOptionResponse]):
    paymentAlert: bool = None
    battleDirectionSkip: bool = None
    battleActionTimeView: bool = None
    @property
    def url(self) -> str:
        return "/api/user/save_option"
class UserApiLoadOptionRequest(RequestBase[UserApiLoadOptionResponse]):
    @property
    def url(self) -> str:
        return "/api/user/load_option"
class UserApiUserSearchRequest(RequestBase[UserApiUserSearchResponse]):
    searchString: str = None
    @property
    def url(self) -> str:
        return "/api/user/user_search"
class UserApiGetUserSubscriptionDataRequest(RequestBase[UserApiGetUserSubscriptionDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_subscription_data"
class UserApiGetUserDisplayInfoListRequest(RequestBase[UserApiGetUserDisplayInfoListResponse]):
    userIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/user/get_user_display_info_list"
class UserApiInitConfigRequest(RequestBase[UserApiInitConfigResponse]):
    @property
    def url(self) -> str:
        return "/api/user/init_config"
class UserApiAccountDeleteRequest(RequestBase[UserApiAccountDeleteResponse]):
    @property
    def url(self) -> str:
        return "/api/user/account_delete"
class UserApiStoreReviewRequest(RequestBase[UserApiStoreReviewResponse]):
    @property
    def url(self) -> str:
        return "/api/user/store_review"
class UserApiGetPlayerIdRequest(RequestBase[UserApiGetPlayerIdResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_player_id"
class PresentApiGetPresentDataListRequest(RequestBase[PresentApiGetPresentDataListResponse]):
    isOrderNewest: bool = None
    expireTimeType: int = None
    @property
    def url(self) -> str:
        return "/api/present/get_present_data_list"
class PresentApiGetReceivedHistoryRequest(RequestBase[PresentApiGetReceivedHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/present/get_received_history"
class PresentApiGetNoReceivedPresentNumRequest(RequestBase[PresentApiGetNoReceivedPresentNumResponse]):
    @property
    def url(self) -> str:
        return "/api/present/get_no_received_present_num"
class PresentApiReceiveRequest(RequestBase[PresentApiReceiveResponse]):
    presentDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/present/receive"
class MissionApiGetMissionDataListRequest(RequestBase[MissionApiGetMissionDataListResponse]):
    missionType: int = None
    @property
    def url(self) -> str:
        return "/api/mission/get_mission_data_list"
class MissionApiReceiveRequest(RequestBase[MissionApiReceiveResponse]):
    missionMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/mission/receive"
class TutorialApiUpdateTutorialStepRequest(RequestBase[TutorialApiUpdateTutorialStepResponse]):
    tutorialStep: int = None
    @property
    def url(self) -> str:
        return "/api/tutorial/update_tutorial_step"
class TutorialApiGetMiniTutorialDataRequest(RequestBase[TutorialApiGetMiniTutorialDataResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/get_mini_tutorial_data"
class TutorialApiExecMiniTutorialRequest(RequestBase[TutorialApiExecMiniTutorialResponse]):
    miniTutorialNumber: int = None
    @property
    def url(self) -> str:
        return "/api/tutorial/exec_mini_tutorial"
class TutorialApiGetPrologueBattleInfoRequest(RequestBase[TutorialApiGetPrologueBattleInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/get_prologue_battle_info"
class TutorialApiSkipTutorialToGachaRequest(RequestBase[TutorialApiSkipTutorialToGachaResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/skip_tutorial_to_gacha"
class ItemApiGetItemDataListRequest(RequestBase[ItemApiGetItemDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/item/get_item_data_list"
class ItemApiGetItemDataListByItemMstIdListRequest(RequestBase[ItemApiGetItemDataListByItemMstIdListResponse]):
    itemMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/item/get_item_data_list_by_item_mst_id_list"
class ItemApiUseItemRequest(RequestBase[ItemApiUseItemResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/item/use_item"
class ItemApiSellItemRequest(RequestBase[ItemApiSellItemResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/item/sell_item"
class HomeApiGetHomeInfoRequest(RequestBase[HomeApiGetHomeInfoResponse]):
    skipLoginBonus: bool = None
    @property
    def url(self) -> str:
        return "/api/home/get_home_info"
class GvgApiGetTopRequest(RequestBase[GvgApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_top"
class GvgApiGetMatchHistoryRequest(RequestBase[GvgApiGetMatchHistoryResponse]):
    viewType: int = None
    day: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_history"
class GvgApiGetMatchDetailHistoryRequest(RequestBase[GvgApiGetMatchDetailHistoryResponse]):
    offenseUserId: int = None
    day: int = None
    allyUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_detail_history"
class GvgApiGetMatchCharacterBuildDetailRequest(RequestBase[GvgApiGetMatchCharacterBuildDetailResponse]):
    day: int = None
    offenseUserId: int = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_character_build_detail"
class GvgApiGetCandidateEnemyUserListRequest(RequestBase[GvgApiGetCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_candidate_enemy_user_list"
class GvgApiGetRankingInfoRequest(RequestBase[GvgApiGetRankingInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_ranking_info"
class GvgApiGetLeagueMatchResultsRequest(RequestBase[GvgApiGetLeagueMatchResultsResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_league_match_results"
class GvgApiGetEnemyUserInfoRequest(RequestBase[GvgApiGetEnemyUserInfoResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_enemy_user_info"
class GvgApiGetTrialEnemyUserInfoRequest(RequestBase[GvgApiGetTrialEnemyUserInfoResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_enemy_user_info"
class GvgApiInitializeStageRequest(RequestBase[GvgApiInitializeStageResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/initialize_stage"
class GvgApiGetGvgInfoRequest(RequestBase[GvgApiGetGvgInfoResponse]):
    roomId: str = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_gvg_info"
class GvgApiRetireRequest(RequestBase[GvgApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/gvg/retire"
class GvgApiGetTrialGvgInfoRequest(RequestBase[GvgApiGetTrialGvgInfoResponse]):
    partyDataId: int = None
    enemyUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_gvg_info"
class GvgApiGetTrialCandidateEnemyUserListRequest(RequestBase[GvgApiGetTrialCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_candidate_enemy_user_list"
class GvgApiFinalizeStageForUserRequest(RequestBase[GvgApiFinalizeStageForUserResponse]):
    roomId: str = None
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/finalize_stage_for_user"
class GveApiGetTopRequest(RequestBase[GveApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_top"
class GveApiGetGuildInfoRequest(RequestBase[GveApiGetGuildInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_guild_info"
class GveApiGetRankingInfoRequest(RequestBase[GveApiGetRankingInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_ranking_info"
class GveApiGetGveHistoryRequest(RequestBase[GveApiGetGveHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_gve_history"
class GveApiInitializeStageRequest(RequestBase[GveApiInitializeStageResponse]):
    gveStageMstId: int = None
    partyDataId: int = None
    enableStrategyBuff: bool = None
    @property
    def url(self) -> str:
        return "/api/gve/initialize_stage"
class GveApiGetGveInfoRequest(RequestBase[GveApiGetGveInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gve/get_gve_info"
class GveApiAddDamageRequest(RequestBase[GveApiAddDamageResponse]):
    questDataId: int = None
    breakCount: int = None
    damageList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/gve/add_damage"
class GveApiFinalizeStageForUserRequest(RequestBase[GveApiFinalizeStageForUserResponse]):
    questDataId: int = None
    totalDamage: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/gve/finalize_stage_for_user"
class GveApiRetireRequest(RequestBase[GveApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/gve/retire"
class GuildApiAppointGuildSubMasterRequest(RequestBase[GuildApiAppointGuildSubMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/appoint_guild_sub_master"
class GuildApiApproveJoinRequestRequest(RequestBase[GuildApiApproveJoinRequestResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/approve_join_request"
class GuildApiApproveScoutRequest(RequestBase[GuildApiApproveScoutResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/approve_scout"
class GuildApiCancelJoinRequestRequest(RequestBase[GuildApiCancelJoinRequestResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/cancel_join_request"
class GuildApiCancelScoutRequest(RequestBase[GuildApiCancelScoutResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/cancel_scout"
class GuildApiGuildNameSearchRequest(RequestBase[GuildApiGuildNameSearchResponse]):
    guildName: str = None
    @property
    def url(self) -> str:
        return "/api/guild/guild_name_search"
class GuildApiConditionalGuildSearchRequest(RequestBase[GuildApiConditionalGuildSearchResponse]):
    guildAtmosphere: int = None
    isAutoApproval: bool = None
    @property
    def url(self) -> str:
        return "/api/guild/conditional_guild_search"
class GuildApiRecommendedGuildSearchRequest(RequestBase[GuildApiRecommendedGuildSearchResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/recommended_guild_search"
class GuildApiCreateGuildRequest(RequestBase[GuildApiCreateGuildResponse]):
    guildName: str = None
    guildDescription: str = None
    isAutoApproval: bool = None
    guildAtmosphere: int = None
    @property
    def url(self) -> str:
        return "/api/guild/create_guild"
class GuildApiDenyJoinRequestRequest(RequestBase[GuildApiDenyJoinRequestResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/deny_join_request"
class GuildApiDenyScoutRequest(RequestBase[GuildApiDenyScoutResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/deny_scout"
class GuildApiExpelGuildMemberRequest(RequestBase[GuildApiExpelGuildMemberResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/expel_guild_member"
class GuildApiGetApplyingJoinRequestListByGuildRequest(RequestBase[GuildApiGetApplyingJoinRequestListByGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_join_request_list_by_guild"
class GuildApiGetApplyingJoinRequestListByUserRequest(RequestBase[GuildApiGetApplyingJoinRequestListByUserResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_join_request_list_by_user"
class GuildApiGetApplyingScoutListByGuildRequest(RequestBase[GuildApiGetApplyingScoutListByGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_scout_list_by_guild"
class GuildApiGetApplyingScoutListByUserRequest(RequestBase[GuildApiGetApplyingScoutListByUserResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_scout_list_by_user"
class GuildApiGetGuildDataRequest(RequestBase[GuildApiGetGuildDataResponse]):
    guildDataId: int = None
    isContainMemberList: bool = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_data"
class GuildApiGetGuildTopInfoRequest(RequestBase[GuildApiGetGuildTopInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_top_info"
class GuildApiGetGuildMemberListRequest(RequestBase[GuildApiGetGuildMemberListResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_member_list"
class GuildApiJoinRequestRequest(RequestBase[GuildApiJoinRequestResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/join_request"
class GuildApiLeaveGuildRequest(RequestBase[GuildApiLeaveGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/leave_guild"
class GuildApiMigrateGuildMasterRequest(RequestBase[GuildApiMigrateGuildMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/migrate_guild_master"
class GuildApiMigrateGuildSubMasterRequest(RequestBase[GuildApiMigrateGuildSubMasterResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/migrate_guild_sub_master"
class GuildApiRemoveGuildRequest(RequestBase[GuildApiRemoveGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/remove_guild"
class GuildApiRemoveGuildSubMasterRequest(RequestBase[GuildApiRemoveGuildSubMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/remove_guild_sub_master"
class GuildApiGetCandidateScoutUserListRequest(RequestBase[GuildApiGetCandidateScoutUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_candidate_scout_user_list"
class GuildApiScoutRequest(RequestBase[GuildApiScoutResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/scout"
class GuildApiSetGuildBasicSettingsRequest(RequestBase[GuildApiSetGuildBasicSettingsResponse]):
    guildName: str = None
    guildDescription: str = None
    guildTitleMstId: int = None
    isAutoApproval: bool = None
    guildAtmosphere: int = None
    @property
    def url(self) -> str:
        return "/api/guild/set_guild_basic_settings"
class GuildApiInstantJoinRequestRequest(RequestBase[GuildApiInstantJoinRequestResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/instant_join_request"
class GuildApiGetGuildTitleDataListRequest(RequestBase[GuildApiGetGuildTitleDataListResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_title_data_list"
class GatheringApiGetGatheringTopRequest(RequestBase[GatheringApiGetGatheringTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/get_gathering_top"
class GatheringApiReceiveRewardRequest(RequestBase[GatheringApiReceiveRewardResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/receive_reward"
class GatheringApiShortcutGatheringRequest(RequestBase[GatheringApiShortcutGatheringResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/shortcut_gathering"
class GachaApiGetGachaTopRequest(RequestBase[GachaApiGetGachaTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gacha/get_gacha_top"
class GachaApiGachaExecRequest(RequestBase[GachaApiGachaExecResponse]):
    gachaMstId: int = None
    @property
    def url(self) -> str:
        return "/api/gacha/gacha_exec"
class GachaApiUpdateAlreadyViewRequest(RequestBase[GachaApiUpdateAlreadyViewResponse]):
    gachaSeriesMstIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/gacha/update_already_view"
class QuestOutGameApiGetUserQuestStageListRequest(RequestBase[QuestOutGameApiGetUserQuestStageListResponse]):
    questCategoryMstId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_quest_stage_list"
class QuestOutGameApiOpenQuestGroupRequest(RequestBase[QuestOutGameApiOpenQuestGroupResponse]):
    questGroupMstId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/open_quest_group"
class QuestOutGameApiGetUserTrainingQuestDataListRequest(RequestBase[QuestOutGameApiGetUserTrainingQuestDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_training_quest_data_list"
class QuestOutGameApiSetUserTrainingQuestRankUpEffectRequest(RequestBase[QuestOutGameApiSetUserTrainingQuestRankUpEffectResponse]):
    questStageMstIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/set_user_training_quest_rank_up_effect"
class QuestOutGameApiGetUserQuestCharacterHeartListRequest(RequestBase[QuestOutGameApiGetUserQuestCharacterHeartListResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_quest_character_heart_list"
class CollectionApiGetCollectionDataListRequest(RequestBase[CollectionApiGetCollectionDataListResponse]):
    objectType: ObjectObjectType = None
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_data_list"
class CollectionApiGetCollectionParamUpAchieveDataListRequest(RequestBase[CollectionApiGetCollectionParamUpAchieveDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_param_up_achieve_data_list"
class CollectionApiUpdateAlreadyViewRequest(RequestBase[CollectionApiUpdateAlreadyViewResponse]):
    objectType: ObjectObjectType = None
    objectIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/collection/update_already_view"
class CollectionApiEndCompleteProgressRequest(RequestBase[CollectionApiEndCompleteProgressResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/end_complete_progress"
class CollectionApiGetMagiaRecordCollectionInfoRequest(RequestBase[CollectionApiGetMagiaRecordCollectionInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/get_magia_record_collection_info"
class CollectionApiAdvReadRequest(RequestBase[CollectionApiAdvReadResponse]):
    advMstIdList: List[int] = None
    skipTypeList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/collection/adv_read"
class CollectionApiGetCollectionIllustAchieveDataRequest(RequestBase[CollectionApiGetCollectionIllustAchieveDataResponse]):
    collectionIllustMstId: int = None
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_illust_achieve_data"
class CollectionApiViewNewCollectionIllustEffectRequest(RequestBase[CollectionApiViewNewCollectionIllustEffectResponse]):
    collectionIllustMstId: int = None
    @property
    def url(self) -> str:
        return "/api/collection/view_new_collection_illust_effect"
class ChatApiCreateGroupChatRoomRequest(RequestBase[ChatApiCreateGroupChatRoomResponse]):
    roomName: str = None
    targetUserIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/chat/create_group_chat_room"
class ChatApiAddUserToGroupChatRoomRequest(RequestBase[ChatApiAddUserToGroupChatRoomResponse]):
    roomDocumentId: str = None
    targetUserIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/chat/add_user_to_group_chat_room"
class ChatApiDeleteUserByGroupChatRoomRequest(RequestBase[ChatApiDeleteUserByGroupChatRoomResponse]):
    roomDocumentId: str = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/delete_user_by_group_chat_room"
class ChatApiLeaveGroupChatRoomRequest(RequestBase[ChatApiLeaveGroupChatRoomResponse]):
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/leave_group_chat_room"
class ChatApiCreateDirectChatRoomRequest(RequestBase[ChatApiCreateDirectChatRoomResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/create_direct_chat_room"
class ChatApiLeaveDirectChatRoomRequest(RequestBase[ChatApiLeaveDirectChatRoomResponse]):
    targetUserId: int = None
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/leave_direct_chat_room"
class ChatApiApproveEnterChatRoomRequest(RequestBase[ChatApiApproveEnterChatRoomResponse]):
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/approve_enter_chat_room"
class ChatApiGetChatBlockUserListRequest(RequestBase[ChatApiGetChatBlockUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/chat/get_chat_block_user_list"
class ChatApiBlockChatUserRequest(RequestBase[ChatApiBlockChatUserResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/block_chat_user"
class ChatApiUnblockChatUserRequest(RequestBase[ChatApiUnblockChatUserResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/unblock_chat_user"
class ChatApiSearchChatUserRequest(RequestBase[ChatApiSearchChatUserResponse]):
    searchString: str = None
    @property
    def url(self) -> str:
        return "/api/chat/search_chat_user"
class PartyApiGetPartyDataListRequest(RequestBase[PartyApiGetPartyDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/party/get_party_data_list"
class PartyApiGetCharacterBuildDataListRequest(RequestBase[PartyApiGetCharacterBuildDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/party/get_character_build_data_list"
class PartyApiSavePartyRequest(RequestBase[PartyApiSavePartyResponse]):
    partyDataId: int = None
    name: str = None
    partyType: int = None
    styleMstId1: int = None
    styleMstId2: int = None
    styleMstId3: int = None
    styleMstId4: int = None
    styleMstId5: int = None
    partyIndex: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party"
class PartyApiSavePartyLeaderRequest(RequestBase[PartyApiSavePartyLeaderResponse]):
    partyDataId: int = None
    styleMstId: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_leader"
class PartyApiSavePartyNameRequest(RequestBase[PartyApiSavePartyNameResponse]):
    partyDataId: int = None
    name: str = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_name"
class PartyApiSavePartyRoleRequest(RequestBase[PartyApiSavePartyRoleResponse]):
    partyDataId: int = None
    role: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_role"
class PartyApiSavePartyForRecommendRequest(RequestBase[PartyApiSavePartyForRecommendResponse]):
    partyType: int = None
    partyDataId: int = None
    partyIndex: int = None
    styleMstId1: int = None
    cardMstId1: int = None
    subStyleMstIds1: List[int] = None
    styleMstId2: int = None
    cardMstId2: int = None
    subStyleMstIds2: List[int] = None
    styleMstId3: int = None
    cardMstId3: int = None
    subStyleMstIds3: List[int] = None
    styleMstId4: int = None
    cardMstId4: int = None
    subStyleMstIds4: List[int] = None
    styleMstId5: int = None
    cardMstId5: int = None
    subStyleMstIds5: List[int] = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_for_recommend"
class PartyApiGetRecommendPartyDataRequest(RequestBase[PartyApiGetRecommendPartyDataResponse]):
    selectedStyleElement: int = None
    selectedParameter: int = None
    isSettingCard: bool = None
    isSettingSubStyle: bool = None
    sameCharacterInParty: bool = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_party_data"
class PartyApiGetRecommendSubStyleRequest(RequestBase[PartyApiGetRecommendSubStyleResponse]):
    characterBuildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_sub_style"
class PartyApiGetRecommendCardRequest(RequestBase[PartyApiGetRecommendCardResponse]):
    characterBuildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_card"
class PartyApiRemovePartyRequest(RequestBase[PartyApiRemovePartyResponse]):
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/remove_party"
class PartyApiSavePartyCardRequest(RequestBase[PartyApiSavePartyCardResponse]):
    partyDataId: int = None
    cardMstId1: int = None
    cardMstId2: int = None
    cardMstId3: int = None
    cardMstId4: int = None
    cardMstId5: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_card"
class PartyApiSavePartySubStyleRequest(RequestBase[PartyApiSavePartySubStyleResponse]):
    partyDataId: int = None
    memberIndex: int = None
    subStyleMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_sub_style"
class CharacterApiGetCharacterListRequest(RequestBase[CharacterApiGetCharacterListResponse]):
    @property
    def url(self) -> str:
        return "/api/character/get_character_list"
class CharacterApiCharacterAwakeRequest(RequestBase[CharacterApiCharacterAwakeResponse]):
    characterMstId: int = None
    onlyItemNum: int = None
    genericItemNum: int = None
    @property
    def url(self) -> str:
        return "/api/character/character_awake"
class CharacterApiCharacterLevelUpRequest(RequestBase[CharacterApiCharacterLevelUpResponse]):
    characterMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/character/character_level_up"
class CharacterApiCharacterHeartLevelUpRequest(RequestBase[CharacterApiCharacterHeartLevelUpResponse]):
    characterMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/character/character_heart_level_up"
class CardApiGetCardListRequest(RequestBase[CardApiGetCardListResponse]):
    @property
    def url(self) -> str:
        return "/api/card/get_card_list"
class CardApiCardLimitBreakRequest(RequestBase[CardApiCardLimitBreakResponse]):
    cardDataId: int = None
    consumeCardDataIds: List[int] = None
    genericItemNum: int = None
    @property
    def url(self) -> str:
        return "/api/card/card_limit_break"
class CardApiCardSellRequest(RequestBase[CardApiCardSellResponse]):
    cardDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/card/card_sell"
class CardApiSetCardProtectRequest(RequestBase[CardApiSetCardProtectResponse]):
    cardDataId: int = None
    isProtect: bool = None
    @property
    def url(self) -> str:
        return "/api/card/set_card_protect"
class CardApiUpdateAlreadyViewRequest(RequestBase[CardApiUpdateAlreadyViewResponse]):
    cardMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/card/update_already_view"
class CardApiCardPassiveSkillLevelUpRequest(RequestBase[CardApiCardPassiveSkillLevelUpResponse]):
    cardMstId: int = None
    passiveSkillLevel: int = None
    @property
    def url(self) -> str:
        return "/api/card/card_passive_skill_level_up"
class QuestBattleApiInitializeStageRequest(RequestBase[QuestBattleApiInitializeStageResponse]):
    questStageMstId: int = None
    partyDataId: int = None
    repeatNum: int = None
    backGroundPlay: bool = None
    isArchiveEvent: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/initialize_stage"
class QuestBattleApiGetQuestInfoRequest(RequestBase[QuestBattleApiGetQuestInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/get_quest_info"
class QuestBattleApiFinalizeStageForUserRequest(RequestBase[QuestBattleApiFinalizeStageForUserResponse]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/finalize_stage_for_user"
class QuestBattleApiRetireRequest(RequestBase[QuestBattleApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/retire"
class QuestBattleApiSkipQuestBattleRequest(RequestBase[QuestBattleApiSkipQuestBattleResponse]):
    questStageMstId: int = None
    partyDataId: int = None
    repeatNum: int = None
    isArchiveEvent: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/skip_quest_battle"
class QuestBattleApiGetBackGroundInfoRequest(RequestBase[QuestBattleApiGetBackGroundInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_battle/get_back_ground_info"
class ExplorationApiGetTopInfoV4Request(RequestBase[ExplorationApiGetTopInfoV4Response]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_top_info_v4"
class ExplorationApiReachFieldPointRequest(RequestBase[ExplorationApiReachFieldPointResponse]):
    fieldPointMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/reach_field_point"
class ExplorationApiOccurDungeonEventRequest(RequestBase[ExplorationApiOccurDungeonEventResponse]):
    fieldStageMstId: int = None
    dungeonEventMstId: int = None
    dungeonRoomMstId: int = None
    presetEventIndex: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/occur_dungeon_event"
class ExplorationApiDungeonStartRequest(RequestBase[ExplorationApiDungeonStartResponse]):
    fieldStageMstId: int = None
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/dungeon_start"
class ExplorationApiDungeonGoalRequest(RequestBase[ExplorationApiDungeonGoalResponse]):
    fieldStageMstId: int = None
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/dungeon_goal"
class ExplorationApiResetDungeonProgressRequest(RequestBase[ExplorationApiResetDungeonProgressResponse]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/reset_dungeon_progress"
class ExplorationApiGetEnableStageListRequest(RequestBase[ExplorationApiGetEnableStageListResponse]):
    @property
    def url(self) -> str:
        return "/api/exploration/get_enable_stage_list"
class ExplorationApiGetStageMstListRequest(RequestBase[ExplorationApiGetStageMstListResponse]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_stage_mst_list"
class ExplorationApiGetDungeonMstListRequest(RequestBase[ExplorationApiGetDungeonMstListResponse]):
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_dungeon_mst_list"
class ExplorationApiGetFieldStageCollectionInfoListRequest(RequestBase[ExplorationApiGetFieldStageCollectionInfoListResponse]):
    @property
    def url(self) -> str:
        return "/api/exploration/get_field_stage_collection_info_list"
class ExplorationApiUpdateUserQuestMapEffectedDataRequest(RequestBase[ExplorationApiUpdateUserQuestMapEffectedDataResponse]):
    questMapMstId: int = None
    difficulty: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/update_user_quest_map_effected_data"
