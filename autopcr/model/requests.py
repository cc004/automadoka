from typing import List, Dict
from .modelbase import Request
from .responses import *
from .common import *
from .enums import *
from pydantic import Field

class WebPlayApiLoginLogRequest(Request[WebPlayApiLoginLogResponse]):
    sessionToken: str = None
    @property
    def url(self) -> str:
        return "/api/web_play/login_log"
class WebPlayApiGetUserMigrationInfoRequest(Request[WebPlayApiGetUserMigrationInfoResponse]):
    sessionToken: str = None
    @property
    def url(self) -> str:
        return "/api/web_play/get_user_migration_info"
class WebPayApiPurchaseRequest(Request[WebPayApiPurchaseResponse]):
    productId: str = None
    @property
    def url(self) -> str:
        return "/api/web_pay/purchase"
class WebPayApiGetPurchaseResultRequest(Request[WebPayApiGetPurchaseResultResponse]):
    purchaseId: str = None
    @property
    def url(self) -> str:
        return "/api/web_pay/get_purchase_result"
class WebPayApiRestoreRequest(Request[WebPayApiRestoreResponse]):
    @property
    def url(self) -> str:
        return "/api/web_pay/restore"
class WebPayApiCancelLatestRequest(Request[WebPayApiCancelLatestResponse]):
    @property
    def url(self) -> str:
        return "/api/web_pay/cancel_latest"
class TitleApiGetTitleTopDataRequest(Request[TitleApiGetTitleTopDataResponse]):
    osType: int = None
    storeType: int = None
    appVersion: str = None
    @property
    def url(self) -> str:
        return "/api/title/get_title_top_data"
class TermsApiGetUpdatedTermsRequest(Request[TermsApiGetUpdatedTermsResponse]):
    storeType: int = None
    @property
    def url(self) -> str:
        return "/api/terms/get_updated_terms"
class TermsApiAgreeLatestTermsRequest(Request[TermsApiAgreeLatestTermsResponse]):
    storeType: int = None
    agreeTermId: int = None
    @property
    def url(self) -> str:
        return "/api/terms/agree_latest_terms"
class TermsApiAgreeChatTermsRequest(Request[TermsApiAgreeChatTermsResponse]):
    @property
    def url(self) -> str:
        return "/api/terms/agree_chat_terms"
class TalismanApiGetTalismanListRequest(Request[TalismanApiGetTalismanListResponse]):
    @property
    def url(self) -> str:
        return "/api/talisman/get_talisman_list"
class TalismanApiTalismanLevelUpRequest(Request[TalismanApiTalismanLevelUpResponse]):
    talismanDataId: int = None
    consumeTalismanDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/talisman/talisman_level_up"
class TalismanApiTalismanSellRequest(Request[TalismanApiTalismanSellResponse]):
    talismanDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/talisman/talisman_sell"
class TalismanApiSetTalismanProtectRequest(Request[TalismanApiSetTalismanProtectResponse]):
    talismanDataId: int = None
    isProtect: bool = None
    @property
    def url(self) -> str:
        return "/api/talisman/set_talisman_protect"
class ServerApiGetTimeZoneInfoRequest(Request[ServerApiGetTimeZoneInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/server/get_time_zone_info"
class ServerApiCertHashListRequest(Request[ServerApiCertHashListResponse]):
    @property
    def url(self) -> str:
        return "/api/server/cert_hash_list"
class SerialCampaignApiInputSerialCodeRequest(Request[SerialCampaignApiInputSerialCodeResponse]):
    serialCode: str = None
    @property
    def url(self) -> str:
        return "/api/serial_campaign/input_serial_code"
class SerialCampaignApiPreAppLinkRequest(Request[SerialCampaignApiPreAppLinkResponse]):
    serialCode: str = None
    @property
    def url(self) -> str:
        return "/api/serial_campaign/pre_app_link"
class SampleApiHttpConnectRequest(Request[SampleApiHttpConnectResponse]):
    @property
    def url(self) -> str:
        return "/api/sample/http_connect"
class NotificationApiRegisterRequest(Request[NotificationApiRegisterResponse]):
    deviceToken: str = None
    @property
    def url(self) -> str:
        return "/api/notification/register"
class NotificationApiSetOsRequest(Request[NotificationApiSetOsResponse]):
    os: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_os"
class NotificationApiSetLanguageRequest(Request[NotificationApiSetLanguageResponse]):
    language: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_language"
class NotificationApiSetRegionRequest(Request[NotificationApiSetRegionResponse]):
    region: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_region"
class NotificationApiSetTimezoneRequest(Request[NotificationApiSetTimezoneResponse]):
    timezone: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_timezone"
class NotificationApiUnsetOsRequest(Request[NotificationApiUnsetOsResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_os"
class NotificationApiUnsetRegionRequest(Request[NotificationApiUnsetRegionResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_region"
class NotificationApiUnsetLanguageRequest(Request[NotificationApiUnsetLanguageResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_language"
class NotificationApiUnsetTimezoneRequest(Request[NotificationApiUnsetTimezoneResponse]):
    @property
    def url(self) -> str:
        return "/api/notification/unset_timezone"
class NotificationApiSetTagRequest(Request[NotificationApiSetTagResponse]):
    tag: str = None
    @property
    def url(self) -> str:
        return "/api/notification/set_tag"
class NotificationApiUnsetTagRequest(Request[NotificationApiUnsetTagResponse]):
    tag: str = None
    @property
    def url(self) -> str:
        return "/api/notification/unset_tag"
class MstApiGetItemMstListRequest(Request[MstApiGetItemMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_item_mst_list"
class MstApiGetCardMstListRequest(Request[MstApiGetCardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_card_mst_list"
class MstApiGetCardLimitBreakMstListRequest(Request[MstApiGetCardLimitBreakMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_card_limit_break_mst_list"
class MstApiGetSkillMstListRequest(Request[MstApiGetSkillMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_mst_list"
class MstApiGetSkillLevelUpConditionMstListRequest(Request[MstApiGetSkillLevelUpConditionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_level_up_condition_mst_list"
class MstApiGetCharacterAwakeMstListRequest(Request[MstApiGetCharacterAwakeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_awake_mst_list"
class MstApiGetCharacterMstListRequest(Request[MstApiGetCharacterMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_mst_list"
class MstApiGetCharacterProfileMstListRequest(Request[MstApiGetCharacterProfileMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_profile_mst_list"
class MstApiGetCharacterHeartMstListRequest(Request[MstApiGetCharacterHeartMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_mst_list"
class MstApiGetCharacterHeartParamUpGroupMstListRequest(Request[MstApiGetCharacterHeartParamUpGroupMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_param_up_group_mst_list"
class MstApiGetCharacterHeartObjectRewardMstListRequest(Request[MstApiGetCharacterHeartObjectRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_object_reward_mst_list"
class MstApiGetCharacterHeartLevelUpMstListRequest(Request[MstApiGetCharacterHeartLevelUpMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_heart_level_up_mst_list"
class MstApiGetCharacterTeamMstListRequest(Request[MstApiGetCharacterTeamMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_character_team_mst_list"
class MstApiGetStyleMstListRequest(Request[MstApiGetStyleMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_mst_list"
class MstApiGetTowerMstListRequest(Request[MstApiGetTowerMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_tower_mst_list"
class MstApiGetQuestCategoryMstListRequest(Request[MstApiGetQuestCategoryMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_category_mst_list"
class MstApiGetQuestMapMstListRequest(Request[MstApiGetQuestMapMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_map_mst_list"
class MstApiGetQuestGroupMstListRequest(Request[MstApiGetQuestGroupMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_group_mst_list"
class MstApiGetQuestStageMstListRequest(Request[MstApiGetQuestStageMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_stage_mst_list"
class MstApiGetQuestConditionMstListRequest(Request[MstApiGetQuestConditionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_condition_mst_list"
class MstApiGetMissionTitleMstListRequest(Request[MstApiGetMissionTitleMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_title_mst_list"
class MstApiGetMissionTransitionMstListRequest(Request[MstApiGetMissionTransitionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_transition_mst_list"
class MstApiGetSubscriptionMissionRewardMstListRequest(Request[MstApiGetSubscriptionMissionRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_subscription_mission_reward_mst_list"
class MstApiGetMissionMstListRequest(Request[MstApiGetMissionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mission_mst_list"
class MstApiGetEnemyMstListRequest(Request[MstApiGetEnemyMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_mst_list"
class MstApiGetEnemyProfileMstListRequest(Request[MstApiGetEnemyProfileMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_profile_mst_list"
class MstApiGetQuestEnemyAppearanceMstListRequest(Request[MstApiGetQuestEnemyAppearanceMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_enemy_appearance_mst_list"
class MstApiGetQuestEnemySkillSetMstListRequest(Request[MstApiGetQuestEnemySkillSetMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_enemy_skill_set_mst_list"
class MstApiGetBreakMstListRequest(Request[MstApiGetBreakMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_break_mst_list"
class MstApiGetAbilityEffectTypeMstListRequest(Request[MstApiGetAbilityEffectTypeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_ability_effect_type_mst_list"
class MstApiGetSkillDetailMstListRequest(Request[MstApiGetSkillDetailMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_skill_detail_mst_list"
class MstApiGetQuestRewardMstListRequest(Request[MstApiGetQuestRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_quest_reward_mst_list"
class MstApiGetFieldSeriesMstListRequest(Request[MstApiGetFieldSeriesMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_series_mst_list"
class MstApiGetFieldStageMstListRequest(Request[MstApiGetFieldStageMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_stage_mst_list"
class MstApiGetAdvMstListRequest(Request[MstApiGetAdvMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_adv_mst_list"
class MstApiGetAdvTitleMstListRequest(Request[MstApiGetAdvTitleMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_adv_title_mst_list"
class MstApiGetObjectReceiveTypeMstListRequest(Request[MstApiGetObjectReceiveTypeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_object_receive_type_mst_list"
class MstApiGetPayTypeMstListRequest(Request[MstApiGetPayTypeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pay_type_mst_list"
class MstApiGetTalismanMstListRequest(Request[MstApiGetTalismanMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_mst_list"
class MstApiGetTalismanParamMstListRequest(Request[MstApiGetTalismanParamMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_param_mst_list"
class MstApiGetTalismanParamEffectMstListRequest(Request[MstApiGetTalismanParamEffectMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_param_effect_mst_list"
class MstApiGetTalismanSeriesMstListRequest(Request[MstApiGetTalismanSeriesMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_talisman_series_mst_list"
class MstApiGetPassiveSkillMstListRequest(Request[MstApiGetPassiveSkillMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_passive_skill_mst_list"
class MstApiGetPassiveSkillDetailMstListRequest(Request[MstApiGetPassiveSkillDetailMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_passive_skill_detail_mst_list"
class MstApiGetLeaderSkillMstListRequest(Request[MstApiGetLeaderSkillMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_leader_skill_mst_list"
class MstApiGetLeaderSkillDetailMstListRequest(Request[MstApiGetLeaderSkillDetailMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_leader_skill_detail_mst_list"
class MstApiGetPvpRankingRewardMstListRequest(Request[MstApiGetPvpRankingRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pvp_ranking_reward_mst_list"
class MstApiGetPvpPointRewardMstListRequest(Request[MstApiGetPvpPointRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_pvp_point_reward_mst_list"
class MstApiGetUserTitleMstListRequest(Request[MstApiGetUserTitleMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_user_title_mst_list"
class MstApiGetGuildTitleMstListRequest(Request[MstApiGetGuildTitleMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_title_mst_list"
class MstApiGetUserLevelUpMstListRequest(Request[MstApiGetUserLevelUpMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_user_level_up_mst_list"
class MstApiGetShopSeriesMstListRequest(Request[MstApiGetShopSeriesMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_series_mst_list"
class MstApiGetShopMstListRequest(Request[MstApiGetShopMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_mst_list"
class MstApiGetShopDetailMstListRequest(Request[MstApiGetShopDetailMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_shop_detail_mst_list"
class MstApiGetBannerMstListRequest(Request[MstApiGetBannerMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_banner_mst_list"
class MstApiGetBannerLabelMstListRequest(Request[MstApiGetBannerLabelMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_banner_label_mst_list"
class MstApiGetHomeBannerMstListRequest(Request[MstApiGetHomeBannerMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_home_banner_mst_list"
class MstApiGetHomeAppealMstListRequest(Request[MstApiGetHomeAppealMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_home_appeal_mst_list"
class MstApiGetTipsMstListRequest(Request[MstApiGetTipsMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_tips_mst_list"
class MstApiGetGveMstListRequest(Request[MstApiGetGveMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_mst_list"
class MstApiGetGveStageMstListRequest(Request[MstApiGetGveStageMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_stage_mst_list"
class MstApiGetGveStageRewardMstListRequest(Request[MstApiGetGveStageRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gve_stage_reward_mst_list"
class MstApiGetMapGveMstListRequest(Request[MstApiGetMapGveMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_mst_list"
class MstApiGetMapGveAreaMstListRequest(Request[MstApiGetMapGveAreaMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_area_mst_list"
class MstApiGetMapGvePointMstListRequest(Request[MstApiGetMapGvePointMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_map_gve_point_mst_list"
class MstApiGetLoginBonusMstListRequest(Request[MstApiGetLoginBonusMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_login_bonus_mst_list"
class MstApiGetLoginBonusRewardMstListRequest(Request[MstApiGetLoginBonusRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_login_bonus_reward_mst_list"
class MstApiGetStyleFigureMstListRequest(Request[MstApiGetStyleFigureMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_figure_mst_list"
class MstApiGetStyleFigureStoryMstListRequest(Request[MstApiGetStyleFigureStoryMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_figure_story_mst_list"
class MstApiGetStyleParamUpTreeMstListRequest(Request[MstApiGetStyleParamUpTreeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_tree_mst_list"
class MstApiGetStyleParamUpMstListRequest(Request[MstApiGetStyleParamUpMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_mst_list"
class MstApiGetStyleParamUpCostMstListRequest(Request[MstApiGetStyleParamUpCostMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_cost_mst_list"
class MstApiGetStyleParamUpEffectMstListRequest(Request[MstApiGetStyleParamUpEffectMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_param_up_effect_mst_list"
class MstApiGetStyleLimitBreakMstListRequest(Request[MstApiGetStyleLimitBreakMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_limit_break_mst_list"
class MstApiGetStyleLimitBreakEffectMstListRequest(Request[MstApiGetStyleLimitBreakEffectMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_limit_break_effect_mst_list"
class MstApiGetStyleLevelUpMstListRequest(Request[MstApiGetStyleLevelUpMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_level_up_mst_list"
class MstApiGetStyleVoiceMstListRequest(Request[MstApiGetStyleVoiceMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_style_voice_mst_list"
class MstApiGetGvgPointRewardMstListRequest(Request[MstApiGetGvgPointRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_point_reward_mst_list"
class MstApiGetGvgRankingRewardMstListRequest(Request[MstApiGetGvgRankingRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_ranking_reward_mst_list"
class MstApiGetChatStampMstListRequest(Request[MstApiGetChatStampMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_chat_stamp_mst_list"
class MstApiGetBattleConditionMstListRequest(Request[MstApiGetBattleConditionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_battle_condition_mst_list"
class MstApiGetBattleConditionSetMstListRequest(Request[MstApiGetBattleConditionSetMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_battle_condition_set_mst_list"
class MstApiGetEnemyConditionSetsAndActionMstListRequest(Request[MstApiGetEnemyConditionSetsAndActionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_enemy_condition_sets_and_action_mst_list"
class MstApiGetDioramaBackgroundMstListRequest(Request[MstApiGetDioramaBackgroundMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_diorama_background_mst_list"
class MstApiGetLive2DParamMstListRequest(Request[MstApiGetLive2DParamMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_live2_d_param_mst_list"
class MstApiGetGvgMstListRequest(Request[MstApiGetGvgMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gvg_mst_list"
class MstApiGetSoundMstListRequest(Request[MstApiGetSoundMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_sound_mst_list"
class MstApiGetCollectionIllustMstListRequest(Request[MstApiGetCollectionIllustMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_illust_mst_list"
class MstApiGetCollectionIllustPieceMstListRequest(Request[MstApiGetCollectionIllustPieceMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_illust_piece_mst_list"
class MstApiGetCollectionParamUpMstListRequest(Request[MstApiGetCollectionParamUpMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_mst_list"
class MstApiGetCollectionParamUpLevelMstListRequest(Request[MstApiGetCollectionParamUpLevelMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_level_mst_list"
class MstApiGetCollectionParamUpEffectMstListRequest(Request[MstApiGetCollectionParamUpEffectMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_param_up_effect_mst_list"
class MstApiGetCollectionConditionGroupMstListRequest(Request[MstApiGetCollectionConditionGroupMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_condition_group_mst_list"
class MstApiGetCollectionConditionMstListRequest(Request[MstApiGetCollectionConditionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_condition_mst_list"
class MstApiGetCollectionRewardMstListRequest(Request[MstApiGetCollectionRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_collection_reward_mst_list"
class MstApiGetStoryEventMstListRequest(Request[MstApiGetStoryEventMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_mst_list"
class MstApiGetStoryEventQuestStageMstListRequest(Request[MstApiGetStoryEventQuestStageMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_quest_stage_mst_list"
class MstApiGetMiniTutorialMstListRequest(Request[MstApiGetMiniTutorialMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_mini_tutorial_mst_list"
class MstApiGetStoryEventScenarioMstListRequest(Request[MstApiGetStoryEventScenarioMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_scenario_mst_list"
class MstApiGetStoryEventScenarioRewardMstListRequest(Request[MstApiGetStoryEventScenarioRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_scenario_reward_mst_list"
class MstApiGetStoryEventBonusRateMstListRequest(Request[MstApiGetStoryEventBonusRateMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_story_event_bonus_rate_mst_list"
class MstApiGetDungeonMstListRequest(Request[MstApiGetDungeonMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_mst_list"
class MstApiGetDungeonTypeMstListRequest(Request[MstApiGetDungeonTypeMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_type_mst_list"
class MstApiGetDungeonRoomMstListRequest(Request[MstApiGetDungeonRoomMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_room_mst_list"
class MstApiGetDungeonEventMstListRequest(Request[MstApiGetDungeonEventMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_dungeon_event_mst_list"
class MstApiGetFieldStratumMstListRequest(Request[MstApiGetFieldStratumMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_stratum_mst_list"
class MstApiGetFieldPointMstListRequest(Request[MstApiGetFieldPointMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_field_point_mst_list"
class MstApiGetBossDirectionMstListRequest(Request[MstApiGetBossDirectionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_boss_direction_mst_list"
class MstApiGetGatheringLevelMstListRequest(Request[MstApiGetGatheringLevelMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gathering_level_mst_list"
class MstApiGetGatheringRewardMstListRequest(Request[MstApiGetGatheringRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_gathering_reward_mst_list"
class MstApiGetScoreAttackMstListRequest(Request[MstApiGetScoreAttackMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_mst_list"
class MstApiGetScoreAttackStageMstListRequest(Request[MstApiGetScoreAttackStageMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_stage_mst_list"
class MstApiGetScoreAttackHighScoreRewardMstListRequest(Request[MstApiGetScoreAttackHighScoreRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_high_score_reward_mst_list"
class MstApiGetScoreAttackTotalScoreRewardMstListRequest(Request[MstApiGetScoreAttackTotalScoreRewardMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_score_attack_total_score_reward_mst_list"
class MstApiGetCalculationPointPolicyMstListRequest(Request[MstApiGetCalculationPointPolicyMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_calculation_point_policy_mst_list"
class MstApiGetGuildMissionMstListRequest(Request[MstApiGetGuildMissionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_mission_mst_list"
class MstApiGetGuildMissionTransitionMstListRequest(Request[MstApiGetGuildMissionTransitionMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/mst/get_guild_mission_transition_mst_list"
class MapGveApiGetTopInfoRequest(Request[MapGveApiGetTopInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/map_gve/get_top_info"
class MapGveApiReachPointRequest(Request[MapGveApiReachPointResponse]):
    mapGvePointMstId: int = None
    @property
    def url(self) -> str:
        return "/api/map_gve/reach_point"
class LoginApiLoginRequest(Request[LoginApiLoginResponse]):
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
class InAppSnsApiCreateLoginUrlRequest(Request[InAppSnsApiCreateLoginUrlResponse]):
    platform: int = None
    @property
    def url(self) -> str:
        return "/api/in_app_sns/create_login_url"
class InAppSnsApiGetAccessTokenRequest(Request[InAppSnsApiGetAccessTokenResponse]):
    state: str = None
    @property
    def url(self) -> str:
        return "/api/in_app_sns/get_access_token"
class HariboteChatApiGetMessageDataListRequest(Request[HariboteChatApiGetMessageDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/haribote_chat/get_message_data_list"
class HariboteChatApiSendMessageRequest(Request[HariboteChatApiSendMessageResponse]):
    message: str = None
    @property
    def url(self) -> str:
        return "/api/debug/haribote_chat/send_message"
class FirestoreApiCreateTokenRequest(Request[FirestoreApiCreateTokenResponse]):
    @property
    def url(self) -> str:
        return "/api/firestore/create_token"
class ExplorationBattleApiInitializeStageV4Request(Request[ExplorationBattleApiInitializeStageV4Response]):
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
class ExplorationBattleApiFinalizeStageForUserV4Request(Request[ExplorationBattleApiFinalizeStageForUserV4Response]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/finalize_stage_for_user_v4"
class ExplorationBattleApiGetExplorationInfoRequest(Request[ExplorationBattleApiGetExplorationInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/get_exploration_info"
class ExplorationBattleApiRetireRequest(Request[ExplorationBattleApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/exploration_battle/retire"
class DebugUserApiRecoverStaminaRequest(Request[DebugUserApiRecoverStaminaResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_user/recover_stamina"
class DebugSubscriptionApiIsValidSubscriptionRequest(Request[DebugSubscriptionApiIsValidSubscriptionResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_subscription/is_valid_subscription"
class DebugSubscriptionApiDoSubscribeForceRequest(Request[DebugSubscriptionApiDoSubscribeForceResponse]):
    @property
    def url(self) -> str:
        return "/api/debug/debug_subscription/do_subscribe_force"
class ConfigApiGetConfigRequest(Request[ConfigApiGetConfigResponse]):
    @property
    def url(self) -> str:
        return "/api/config/get_config"
class AppVersionApiGetReviewVersionDataRequest(Request[AppVersionApiGetReviewVersionDataResponse]):
    storeType: int = None
    appVersion: str = None
    @property
    def url(self) -> str:
        return "/api/app_version/get_review_version_data"
class AkamaiApiCreateTokenRequest(Request[AkamaiApiCreateTokenResponse]):
    @property
    def url(self) -> str:
        return "/api/akamai/create_token"
class TowerApiGetTowerTopRequest(Request[TowerApiGetTowerTopResponse]):
    @property
    def url(self) -> str:
        return "/api/tower/get_tower_top"
class TowerApiRecoverySkipNumRequest(Request[TowerApiRecoverySkipNumResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/tower/recovery_skip_num"
class TowerApiSkipQuestBattleRequest(Request[TowerApiSkipQuestBattleResponse]):
    questStageMstId: int = None
    repeatNum: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/tower/skip_quest_battle"
class StyleApiGetStyleDataListRequest(Request[StyleApiGetStyleDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/style/get_style_data_list"
class StyleApiStyleLevelUpRequest(Request[StyleApiStyleLevelUpResponse]):
    styleMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/style/style_level_up"
class StyleApiStyleLevelUpVer2Request(Request[StyleApiStyleLevelUpVer2Response]):
    styleMstId: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_level_up_ver2"
class StyleApiStyleSkillLevelUpRequest(Request[StyleApiStyleSkillLevelUpResponse]):
    styleMstId: int = None
    skillLevelUpType: int = None
    skillNo: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_skill_level_up"
class StyleApiStyleSpecialAttackSkillLevelUpRequest(Request[StyleApiStyleSpecialAttackSkillLevelUpResponse]):
    styleMstId: int = None
    level: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_special_attack_skill_level_up"
class StyleApiStyleLimitBreakRequest(Request[StyleApiStyleLimitBreakResponse]):
    styleMstId: int = None
    itemNum: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_limit_break"
class StyleApiOpenStyleParamUpTreeRequest(Request[StyleApiOpenStyleParamUpTreeResponse]):
    styleMstId: int = None
    styleParamUpTreeMstId: int = None
    @property
    def url(self) -> str:
        return "/api/style/open_style_param_up_tree"
class StyleApiStyleParamUpRequest(Request[StyleApiStyleParamUpResponse]):
    styleMstId: int = None
    styleParamUpTreeMstId: int = None
    paramUpType: int = None
    @property
    def url(self) -> str:
        return "/api/style/style_param_up"
class StyleApiUpdateAlreadyViewRequest(Request[StyleApiUpdateAlreadyViewResponse]):
    styleMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/style/update_already_view"
class StoryEventApiGetTopRequest(Request[StoryEventApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/story_event/get_top"
class StoryEventApiGetArchiveEventListRequest(Request[StoryEventApiGetArchiveEventListResponse]):
    @property
    def url(self) -> str:
        return "/api/story_event/get_archive_event_list"
class StoryEventApiOpenStoryRequest(Request[StoryEventApiOpenStoryResponse]):
    storyEventMstId: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/open_story"
class StoryEventApiScenarioReadRequest(Request[StoryEventApiScenarioReadResponse]):
    storyEventScenarioMstId: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/scenario_read"
class StoryEventApiRecoverPlayableCountRequest(Request[StoryEventApiRecoverPlayableCountResponse]):
    storyEventMstId: int = None
    recoverCount: int = None
    @property
    def url(self) -> str:
        return "/api/story_event/recover_playable_count"
class ShopApiGetShopListRequest(Request[ShopApiGetShopListResponse]):
    @property
    def url(self) -> str:
        return "/api/shop/get_shop_list"
class ShopApiBuyRequest(Request[ShopApiBuyResponse]):
    shopMstId: int = None
    shopSeriesMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/shop/buy"
class ShopApiGetShopPaymentMstListRequest(Request[ShopApiGetShopPaymentMstListResponse]):
    @property
    def url(self) -> str:
        return "/api/shop/get_shop_payment_mst_list"
class ScoreAttackApiGetScoreAttackTopRequest(Request[ScoreAttackApiGetScoreAttackTopResponse]):
    scoreAttackMstId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_score_attack_top"
class ScoreAttackApiGetRankingInfoRequest(Request[ScoreAttackApiGetRankingInfoResponse]):
    scoreAttackMstId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_ranking_info"
class ScoreAttackApiInitializeStageRequest(Request[ScoreAttackApiInitializeStageResponse]):
    scoreAttackStageMstId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/initialize_stage"
class ScoreAttackApiGetScoreAttackInfoRequest(Request[ScoreAttackApiGetScoreAttackInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/get_score_attack_info"
class ScoreAttackApiFinalizeStageForUserRequest(Request[ScoreAttackApiFinalizeStageForUserResponse]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/score_attack/finalize_stage_for_user"
class ScoreAttackApiRetireRequest(Request[ScoreAttackApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/score_attack/retire"
class PvpApiGetPvpTopRequest(Request[PvpApiGetPvpTopResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_pvp_top"
class PvpApiGetRankingInfoRequest(Request[PvpApiGetRankingInfoResponse]):
    mode: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_ranking_info"
class PvpApiGetCandidateEnemyUserListRequest(Request[PvpApiGetCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_candidate_enemy_user_list"
class PvpApiGetEnemyUserInfoRequest(Request[PvpApiGetEnemyUserInfoResponse]):
    chooseEnemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_enemy_user_info"
class PvpApiInitializeStageRequest(Request[PvpApiInitializeStageResponse]):
    chooseEnemyUserId: int = None
    partyDataId: int = None
    isConsumeGem: bool = None
    @property
    def url(self) -> str:
        return "/api/pvp/initialize_stage"
class PvpApiRetireRequest(Request[PvpApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/pvp/retire"
class PvpApiGetPvpInfoRequest(Request[PvpApiGetPvpInfoResponse]):
    roomId: str = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_pvp_info"
class PvpApiFinalizeStageRequest(Request[PvpApiFinalizeStageResponse]):
    roomId: str = None
    winUserId: int = None
    result: int = None
    battleLog: str = None
    @property
    def url(self) -> str:
        return "/api/pvp/finalize_stage"
class PvpApiFinalizeStageForUserRequest(Request[PvpApiFinalizeStageForUserResponse]):
    roomId: str = None
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/finalize_stage_for_user"
class PvpApiGetMatchHistoryRequest(Request[PvpApiGetMatchHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_history"
class PvpApiGetMatchDetailHistoryRequest(Request[PvpApiGetMatchDetailHistoryResponse]):
    pvpDataId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_detail_history"
class PvpApiGetMatchCharacterBuildDetailRequest(Request[PvpApiGetMatchCharacterBuildDetailResponse]):
    pvpDataId: int = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_match_character_build_detail"
class PvpApiGetRankingUserCharacterBuildDetailRequest(Request[PvpApiGetRankingUserCharacterBuildDetailResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/pvp/get_ranking_user_character_build_detail"
class UserTitleApiGetUserTitleDataListRequest(Request[UserTitleApiGetUserTitleDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/user_title/get_user_title_data_list"
class UserApiGetUserDataRequest(Request[UserApiGetUserDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_data"
class UserApiGetUserParamDataRequest(Request[UserApiGetUserParamDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_param_data"
class UserApiGetInitDataListRequest(Request[UserApiGetInitDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_init_data_list"
class UserApiGetUserProfileDataRequest(Request[UserApiGetUserProfileDataResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_user_profile_data"
class UserApiGetOtherUserProfileDataRequest(Request[UserApiGetOtherUserProfileDataResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_other_user_profile_data"
class UserApiSetNameRequest(Request[UserApiSetNameResponse]):
    name: str = None
    @property
    def url(self) -> str:
        return "/api/user/set_name"
class UserApiSetCommentRequest(Request[UserApiSetCommentResponse]):
    comment: str = None
    @property
    def url(self) -> str:
        return "/api/user/set_comment"
class UserApiSetFavoriteInfoRequest(Request[UserApiSetFavoriteInfoResponse]):
    characterMstId: int = None
    styleMstId: int = None
    skillMstId: int = None
    @property
    def url(self) -> str:
        return "/api/user/set_favorite_info"
class UserApiSetDisplayUserTitleRequest(Request[UserApiSetDisplayUserTitleResponse]):
    userTitleMstIds: List[int] = None
    value1List: List[int] = None
    @property
    def url(self) -> str:
        return "/api/user/set_display_user_title"
class UserApiSetStaminaRecoverRequest(Request[UserApiSetStaminaRecoverResponse]):
    recoverType: int = None
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/user/set_stamina_recover"
class UserApiSaveOptionRequest(Request[UserApiSaveOptionResponse]):
    paymentAlert: bool = None
    battleDirectionSkip: bool = None
    battleActionTimeView: bool = None
    @property
    def url(self) -> str:
        return "/api/user/save_option"
class UserApiLoadOptionRequest(Request[UserApiLoadOptionResponse]):
    @property
    def url(self) -> str:
        return "/api/user/load_option"
class UserApiUserSearchRequest(Request[UserApiUserSearchResponse]):
    searchString: str = None
    @property
    def url(self) -> str:
        return "/api/user/user_search"
class UserApiGetUserSubscriptionDataRequest(Request[UserApiGetUserSubscriptionDataResponse]):
    @property
    def url(self) -> str:
        return "/api/user/get_user_subscription_data"
class UserApiGetUserDisplayInfoListRequest(Request[UserApiGetUserDisplayInfoListResponse]):
    userIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/user/get_user_display_info_list"
class UserApiInitConfigRequest(Request[UserApiInitConfigResponse]):
    @property
    def url(self) -> str:
        return "/api/user/init_config"
class UserApiAccountDeleteRequest(Request[UserApiAccountDeleteResponse]):
    @property
    def url(self) -> str:
        return "/api/user/account_delete"
class UserApiStoreReviewRequest(Request[UserApiStoreReviewResponse]):
    @property
    def url(self) -> str:
        return "/api/user/store_review"
class UserApiGetPlayerIdRequest(Request[UserApiGetPlayerIdResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/user/get_player_id"
class PresentApiGetPresentDataListRequest(Request[PresentApiGetPresentDataListResponse]):
    isOrderNewest: bool = None
    expireTimeType: int = None
    @property
    def url(self) -> str:
        return "/api/present/get_present_data_list"
class PresentApiGetReceivedHistoryRequest(Request[PresentApiGetReceivedHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/present/get_received_history"
class PresentApiGetNoReceivedPresentNumRequest(Request[PresentApiGetNoReceivedPresentNumResponse]):
    @property
    def url(self) -> str:
        return "/api/present/get_no_received_present_num"
class PresentApiReceiveRequest(Request[PresentApiReceiveResponse]):
    presentDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/present/receive"
class MissionApiGetMissionDataListRequest(Request[MissionApiGetMissionDataListResponse]):
    missionType: int = None
    @property
    def url(self) -> str:
        return "/api/mission/get_mission_data_list"
class MissionApiReceiveRequest(Request[MissionApiReceiveResponse]):
    missionMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/mission/receive"
class TutorialApiUpdateTutorialStepRequest(Request[TutorialApiUpdateTutorialStepResponse]):
    tutorialStep: int = None
    @property
    def url(self) -> str:
        return "/api/tutorial/update_tutorial_step"
class TutorialApiGetMiniTutorialDataRequest(Request[TutorialApiGetMiniTutorialDataResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/get_mini_tutorial_data"
class TutorialApiExecMiniTutorialRequest(Request[TutorialApiExecMiniTutorialResponse]):
    miniTutorialNumber: int = None
    @property
    def url(self) -> str:
        return "/api/tutorial/exec_mini_tutorial"
class TutorialApiGetPrologueBattleInfoRequest(Request[TutorialApiGetPrologueBattleInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/get_prologue_battle_info"
class TutorialApiSkipTutorialToGachaRequest(Request[TutorialApiSkipTutorialToGachaResponse]):
    @property
    def url(self) -> str:
        return "/api/tutorial/skip_tutorial_to_gacha"
class ItemApiGetItemDataListRequest(Request[ItemApiGetItemDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/item/get_item_data_list"
class ItemApiGetItemDataListByItemMstIdListRequest(Request[ItemApiGetItemDataListByItemMstIdListResponse]):
    itemMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/item/get_item_data_list_by_item_mst_id_list"
class ItemApiUseItemRequest(Request[ItemApiUseItemResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/item/use_item"
class ItemApiSellItemRequest(Request[ItemApiSellItemResponse]):
    itemMstId: int = None
    num: int = None
    @property
    def url(self) -> str:
        return "/api/item/sell_item"
class HomeApiGetHomeInfoRequest(Request[HomeApiGetHomeInfoResponse]):
    skipLoginBonus: bool = None
    @property
    def url(self) -> str:
        return "/api/home/get_home_info"
class GvgApiGetTopRequest(Request[GvgApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_top"
class GvgApiGetMatchHistoryRequest(Request[GvgApiGetMatchHistoryResponse]):
    viewType: int = None
    day: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_history"
class GvgApiGetMatchDetailHistoryRequest(Request[GvgApiGetMatchDetailHistoryResponse]):
    offenseUserId: int = None
    day: int = None
    allyUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_detail_history"
class GvgApiGetMatchCharacterBuildDetailRequest(Request[GvgApiGetMatchCharacterBuildDetailResponse]):
    day: int = None
    offenseUserId: int = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_match_character_build_detail"
class GvgApiGetCandidateEnemyUserListRequest(Request[GvgApiGetCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_candidate_enemy_user_list"
class GvgApiGetRankingInfoRequest(Request[GvgApiGetRankingInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_ranking_info"
class GvgApiGetLeagueMatchResultsRequest(Request[GvgApiGetLeagueMatchResultsResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_league_match_results"
class GvgApiGetEnemyUserInfoRequest(Request[GvgApiGetEnemyUserInfoResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_enemy_user_info"
class GvgApiGetTrialEnemyUserInfoRequest(Request[GvgApiGetTrialEnemyUserInfoResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_enemy_user_info"
class GvgApiInitializeStageRequest(Request[GvgApiInitializeStageResponse]):
    enemyUserId: int = None
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/initialize_stage"
class GvgApiGetGvgInfoRequest(Request[GvgApiGetGvgInfoResponse]):
    roomId: str = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_gvg_info"
class GvgApiRetireRequest(Request[GvgApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/gvg/retire"
class GvgApiGetTrialGvgInfoRequest(Request[GvgApiGetTrialGvgInfoResponse]):
    partyDataId: int = None
    enemyUserId: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_gvg_info"
class GvgApiGetTrialCandidateEnemyUserListRequest(Request[GvgApiGetTrialCandidateEnemyUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/gvg/get_trial_candidate_enemy_user_list"
class GvgApiFinalizeStageForUserRequest(Request[GvgApiFinalizeStageForUserResponse]):
    roomId: str = None
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/gvg/finalize_stage_for_user"
class GveApiGetTopRequest(Request[GveApiGetTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_top"
class GveApiGetGuildInfoRequest(Request[GveApiGetGuildInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_guild_info"
class GveApiGetRankingInfoRequest(Request[GveApiGetRankingInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_ranking_info"
class GveApiGetGveHistoryRequest(Request[GveApiGetGveHistoryResponse]):
    @property
    def url(self) -> str:
        return "/api/gve/get_gve_history"
class GveApiInitializeStageRequest(Request[GveApiInitializeStageResponse]):
    gveStageMstId: int = None
    partyDataId: int = None
    enableStrategyBuff: bool = None
    @property
    def url(self) -> str:
        return "/api/gve/initialize_stage"
class GveApiGetGveInfoRequest(Request[GveApiGetGveInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/gve/get_gve_info"
class GveApiAddDamageRequest(Request[GveApiAddDamageResponse]):
    questDataId: int = None
    breakCount: int = None
    damageList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/gve/add_damage"
class GveApiFinalizeStageForUserRequest(Request[GveApiFinalizeStageForUserResponse]):
    questDataId: int = None
    totalDamage: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/gve/finalize_stage_for_user"
class GveApiRetireRequest(Request[GveApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/gve/retire"
class GuildApiAppointGuildSubMasterRequest(Request[GuildApiAppointGuildSubMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/appoint_guild_sub_master"
class GuildApiApproveJoinRequestRequest(Request[GuildApiApproveJoinRequestResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/approve_join_request"
class GuildApiApproveScoutRequest(Request[GuildApiApproveScoutResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/approve_scout"
class GuildApiCancelJoinRequestRequest(Request[GuildApiCancelJoinRequestResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/cancel_join_request"
class GuildApiCancelScoutRequest(Request[GuildApiCancelScoutResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/cancel_scout"
class GuildApiGuildNameSearchRequest(Request[GuildApiGuildNameSearchResponse]):
    guildName: str = None
    @property
    def url(self) -> str:
        return "/api/guild/guild_name_search"
class GuildApiConditionalGuildSearchRequest(Request[GuildApiConditionalGuildSearchResponse]):
    guildAtmosphere: int = None
    isAutoApproval: bool = None
    @property
    def url(self) -> str:
        return "/api/guild/conditional_guild_search"
class GuildApiRecommendedGuildSearchRequest(Request[GuildApiRecommendedGuildSearchResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/recommended_guild_search"
class GuildApiCreateGuildRequest(Request[GuildApiCreateGuildResponse]):
    guildName: str = None
    guildDescription: str = None
    isAutoApproval: bool = None
    guildAtmosphere: int = None
    @property
    def url(self) -> str:
        return "/api/guild/create_guild"
class GuildApiDenyJoinRequestRequest(Request[GuildApiDenyJoinRequestResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/deny_join_request"
class GuildApiDenyScoutRequest(Request[GuildApiDenyScoutResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/deny_scout"
class GuildApiExpelGuildMemberRequest(Request[GuildApiExpelGuildMemberResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/expel_guild_member"
class GuildApiGetApplyingJoinRequestListByGuildRequest(Request[GuildApiGetApplyingJoinRequestListByGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_join_request_list_by_guild"
class GuildApiGetApplyingJoinRequestListByUserRequest(Request[GuildApiGetApplyingJoinRequestListByUserResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_join_request_list_by_user"
class GuildApiGetApplyingScoutListByGuildRequest(Request[GuildApiGetApplyingScoutListByGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_scout_list_by_guild"
class GuildApiGetApplyingScoutListByUserRequest(Request[GuildApiGetApplyingScoutListByUserResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_applying_scout_list_by_user"
class GuildApiGetGuildDataRequest(Request[GuildApiGetGuildDataResponse]):
    guildDataId: int = None
    isContainMemberList: bool = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_data"
class GuildApiGetGuildTopInfoRequest(Request[GuildApiGetGuildTopInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_top_info"
class GuildApiGetGuildMemberListRequest(Request[GuildApiGetGuildMemberListResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_member_list"
class GuildApiJoinRequestRequest(Request[GuildApiJoinRequestResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/join_request"
class GuildApiLeaveGuildRequest(Request[GuildApiLeaveGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/leave_guild"
class GuildApiMigrateGuildMasterRequest(Request[GuildApiMigrateGuildMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/migrate_guild_master"
class GuildApiMigrateGuildSubMasterRequest(Request[GuildApiMigrateGuildSubMasterResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/migrate_guild_sub_master"
class GuildApiRemoveGuildRequest(Request[GuildApiRemoveGuildResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/remove_guild"
class GuildApiRemoveGuildSubMasterRequest(Request[GuildApiRemoveGuildSubMasterResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/remove_guild_sub_master"
class GuildApiGetCandidateScoutUserListRequest(Request[GuildApiGetCandidateScoutUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/get_candidate_scout_user_list"
class GuildApiScoutRequest(Request[GuildApiScoutResponse]):
    userId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/scout"
class GuildApiSetGuildBasicSettingsRequest(Request[GuildApiSetGuildBasicSettingsResponse]):
    guildName: str = None
    guildDescription: str = None
    guildTitleMstId: int = None
    isAutoApproval: bool = None
    guildAtmosphere: int = None
    @property
    def url(self) -> str:
        return "/api/guild/set_guild_basic_settings"
class GuildApiInstantJoinRequestRequest(Request[GuildApiInstantJoinRequestResponse]):
    @property
    def url(self) -> str:
        return "/api/guild/instant_join_request"
class GuildApiGetGuildTitleDataListRequest(Request[GuildApiGetGuildTitleDataListResponse]):
    guildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/guild/get_guild_title_data_list"
class GatheringApiGetGatheringTopRequest(Request[GatheringApiGetGatheringTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/get_gathering_top"
class GatheringApiReceiveRewardRequest(Request[GatheringApiReceiveRewardResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/receive_reward"
class GatheringApiShortcutGatheringRequest(Request[GatheringApiShortcutGatheringResponse]):
    @property
    def url(self) -> str:
        return "/api/gathering/shortcut_gathering"
class GachaApiGetGachaTopRequest(Request[GachaApiGetGachaTopResponse]):
    @property
    def url(self) -> str:
        return "/api/gacha/get_gacha_top"
class GachaApiGachaExecRequest(Request[GachaApiGachaExecResponse]):
    gachaMstId: int = None
    @property
    def url(self) -> str:
        return "/api/gacha/gacha_exec"
class GachaApiUpdateAlreadyViewRequest(Request[GachaApiUpdateAlreadyViewResponse]):
    gachaSeriesMstIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/gacha/update_already_view"
class QuestOutGameApiGetUserQuestStageListRequest(Request[QuestOutGameApiGetUserQuestStageListResponse]):
    questCategoryMstId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_quest_stage_list"
class QuestOutGameApiOpenQuestGroupRequest(Request[QuestOutGameApiOpenQuestGroupResponse]):
    questGroupMstId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/open_quest_group"
class QuestOutGameApiGetUserTrainingQuestDataListRequest(Request[QuestOutGameApiGetUserTrainingQuestDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_training_quest_data_list"
class QuestOutGameApiSetUserTrainingQuestRankUpEffectRequest(Request[QuestOutGameApiSetUserTrainingQuestRankUpEffectResponse]):
    questStageMstIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/quest_out_game/set_user_training_quest_rank_up_effect"
class QuestOutGameApiGetUserQuestCharacterHeartListRequest(Request[QuestOutGameApiGetUserQuestCharacterHeartListResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_out_game/get_user_quest_character_heart_list"
class CollectionApiGetCollectionDataListRequest(Request[CollectionApiGetCollectionDataListResponse]):
    objectType: ObjectObjectType = None
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_data_list"
class CollectionApiGetCollectionParamUpAchieveDataListRequest(Request[CollectionApiGetCollectionParamUpAchieveDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_param_up_achieve_data_list"
class CollectionApiUpdateAlreadyViewRequest(Request[CollectionApiUpdateAlreadyViewResponse]):
    objectType: ObjectObjectType = None
    objectIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/collection/update_already_view"
class CollectionApiEndCompleteProgressRequest(Request[CollectionApiEndCompleteProgressResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/end_complete_progress"
class CollectionApiGetMagiaRecordCollectionInfoRequest(Request[CollectionApiGetMagiaRecordCollectionInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/collection/get_magia_record_collection_info"
class CollectionApiAdvReadRequest(Request[CollectionApiAdvReadResponse]):
    advMstIdList: List[int] = None
    skipTypeList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/collection/adv_read"
class CollectionApiGetCollectionIllustAchieveDataRequest(Request[CollectionApiGetCollectionIllustAchieveDataResponse]):
    collectionIllustMstId: int = None
    @property
    def url(self) -> str:
        return "/api/collection/get_collection_illust_achieve_data"
class CollectionApiViewNewCollectionIllustEffectRequest(Request[CollectionApiViewNewCollectionIllustEffectResponse]):
    collectionIllustMstId: int = None
    @property
    def url(self) -> str:
        return "/api/collection/view_new_collection_illust_effect"
class ChatApiCreateGroupChatRoomRequest(Request[ChatApiCreateGroupChatRoomResponse]):
    roomName: str = None
    targetUserIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/chat/create_group_chat_room"
class ChatApiAddUserToGroupChatRoomRequest(Request[ChatApiAddUserToGroupChatRoomResponse]):
    roomDocumentId: str = None
    targetUserIdList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/chat/add_user_to_group_chat_room"
class ChatApiDeleteUserByGroupChatRoomRequest(Request[ChatApiDeleteUserByGroupChatRoomResponse]):
    roomDocumentId: str = None
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/delete_user_by_group_chat_room"
class ChatApiLeaveGroupChatRoomRequest(Request[ChatApiLeaveGroupChatRoomResponse]):
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/leave_group_chat_room"
class ChatApiCreateDirectChatRoomRequest(Request[ChatApiCreateDirectChatRoomResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/create_direct_chat_room"
class ChatApiLeaveDirectChatRoomRequest(Request[ChatApiLeaveDirectChatRoomResponse]):
    targetUserId: int = None
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/leave_direct_chat_room"
class ChatApiApproveEnterChatRoomRequest(Request[ChatApiApproveEnterChatRoomResponse]):
    roomDocumentId: str = None
    @property
    def url(self) -> str:
        return "/api/chat/approve_enter_chat_room"
class ChatApiGetChatBlockUserListRequest(Request[ChatApiGetChatBlockUserListResponse]):
    @property
    def url(self) -> str:
        return "/api/chat/get_chat_block_user_list"
class ChatApiBlockChatUserRequest(Request[ChatApiBlockChatUserResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/block_chat_user"
class ChatApiUnblockChatUserRequest(Request[ChatApiUnblockChatUserResponse]):
    targetUserId: int = None
    @property
    def url(self) -> str:
        return "/api/chat/unblock_chat_user"
class ChatApiSearchChatUserRequest(Request[ChatApiSearchChatUserResponse]):
    searchString: str = None
    @property
    def url(self) -> str:
        return "/api/chat/search_chat_user"
class PartyApiGetPartyDataListRequest(Request[PartyApiGetPartyDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/party/get_party_data_list"
class PartyApiGetCharacterBuildDataListRequest(Request[PartyApiGetCharacterBuildDataListResponse]):
    @property
    def url(self) -> str:
        return "/api/party/get_character_build_data_list"
class PartyApiSavePartyRequest(Request[PartyApiSavePartyResponse]):
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
class PartyApiSavePartyLeaderRequest(Request[PartyApiSavePartyLeaderResponse]):
    partyDataId: int = None
    styleMstId: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_leader"
class PartyApiSavePartyNameRequest(Request[PartyApiSavePartyNameResponse]):
    partyDataId: int = None
    name: str = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_name"
class PartyApiSavePartyRoleRequest(Request[PartyApiSavePartyRoleResponse]):
    partyDataId: int = None
    role: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_role"
class PartyApiSavePartyForRecommendRequest(Request[PartyApiSavePartyForRecommendResponse]):
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
class PartyApiGetRecommendPartyDataRequest(Request[PartyApiGetRecommendPartyDataResponse]):
    selectedStyleElement: int = None
    selectedParameter: int = None
    isSettingCard: bool = None
    isSettingSubStyle: bool = None
    sameCharacterInParty: bool = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_party_data"
class PartyApiGetRecommendSubStyleRequest(Request[PartyApiGetRecommendSubStyleResponse]):
    characterBuildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_sub_style"
class PartyApiGetRecommendCardRequest(Request[PartyApiGetRecommendCardResponse]):
    characterBuildDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/get_recommend_card"
class PartyApiRemovePartyRequest(Request[PartyApiRemovePartyResponse]):
    partyDataId: int = None
    @property
    def url(self) -> str:
        return "/api/party/remove_party"
class PartyApiSavePartyCardRequest(Request[PartyApiSavePartyCardResponse]):
    partyDataId: int = None
    cardMstId1: int = None
    cardMstId2: int = None
    cardMstId3: int = None
    cardMstId4: int = None
    cardMstId5: int = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_card"
class PartyApiSavePartySubStyleRequest(Request[PartyApiSavePartySubStyleResponse]):
    partyDataId: int = None
    memberIndex: int = None
    subStyleMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/party/save_party_sub_style"
class CharacterApiGetCharacterListRequest(Request[CharacterApiGetCharacterListResponse]):
    @property
    def url(self) -> str:
        return "/api/character/get_character_list"
class CharacterApiCharacterAwakeRequest(Request[CharacterApiCharacterAwakeResponse]):
    characterMstId: int = None
    onlyItemNum: int = None
    genericItemNum: int = None
    @property
    def url(self) -> str:
        return "/api/character/character_awake"
class CharacterApiCharacterLevelUpRequest(Request[CharacterApiCharacterLevelUpResponse]):
    characterMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/character/character_level_up"
class CharacterApiCharacterHeartLevelUpRequest(Request[CharacterApiCharacterHeartLevelUpResponse]):
    characterMstId: int = None
    itemMstIdList: List[int] = None
    itemNumList: List[int] = None
    @property
    def url(self) -> str:
        return "/api/character/character_heart_level_up"
class CardApiGetCardListRequest(Request[CardApiGetCardListResponse]):
    @property
    def url(self) -> str:
        return "/api/card/get_card_list"
class CardApiCardLimitBreakRequest(Request[CardApiCardLimitBreakResponse]):
    cardDataId: int = None
    consumeCardDataIds: List[int] = None
    genericItemNum: int = None
    @property
    def url(self) -> str:
        return "/api/card/card_limit_break"
class CardApiCardSellRequest(Request[CardApiCardSellResponse]):
    cardDataIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/card/card_sell"
class CardApiSetCardProtectRequest(Request[CardApiSetCardProtectResponse]):
    cardDataId: int = None
    isProtect: bool = None
    @property
    def url(self) -> str:
        return "/api/card/set_card_protect"
class CardApiUpdateAlreadyViewRequest(Request[CardApiUpdateAlreadyViewResponse]):
    cardMstIds: List[int] = None
    @property
    def url(self) -> str:
        return "/api/card/update_already_view"
class CardApiCardPassiveSkillLevelUpRequest(Request[CardApiCardPassiveSkillLevelUpResponse]):
    cardMstId: int = None
    passiveSkillLevel: int = None
    @property
    def url(self) -> str:
        return "/api/card/card_passive_skill_level_up"
class QuestBattleApiInitializeStageRequest(Request[QuestBattleApiInitializeStageResponse]):
    questStageMstId: int = None
    partyDataId: int = None
    repeatNum: int = None
    backGroundPlay: bool = None
    isArchiveEvent: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/initialize_stage"
class QuestBattleApiGetQuestInfoRequest(Request[QuestBattleApiGetQuestInfoResponse]):
    questDataId: int = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/get_quest_info"
class QuestBattleApiFinalizeStageForUserRequest(Request[QuestBattleApiFinalizeStageForUserResponse]):
    result: int = None
    battleLog: str = None
    autoMode: int = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/finalize_stage_for_user"
class QuestBattleApiRetireRequest(Request[QuestBattleApiRetireResponse]):
    battleLog: str = None
    isSystemRetire: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/retire"
class QuestBattleApiSkipQuestBattleRequest(Request[QuestBattleApiSkipQuestBattleResponse]):
    questStageMstId: int = None
    partyDataId: int = None
    repeatNum: int = None
    isArchiveEvent: bool = None
    @property
    def url(self) -> str:
        return "/api/quest_battle/skip_quest_battle"
class QuestBattleApiGetBackGroundInfoRequest(Request[QuestBattleApiGetBackGroundInfoResponse]):
    @property
    def url(self) -> str:
        return "/api/quest_battle/get_back_ground_info"
class ExplorationApiGetTopInfoV4Request(Request[ExplorationApiGetTopInfoV4Response]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_top_info_v4"
class ExplorationApiReachFieldPointRequest(Request[ExplorationApiReachFieldPointResponse]):
    fieldPointMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/reach_field_point"
class ExplorationApiOccurDungeonEventRequest(Request[ExplorationApiOccurDungeonEventResponse]):
    fieldStageMstId: int = None
    dungeonEventMstId: int = None
    dungeonRoomMstId: int = None
    presetEventIndex: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/occur_dungeon_event"
class ExplorationApiDungeonStartRequest(Request[ExplorationApiDungeonStartResponse]):
    fieldStageMstId: int = None
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/dungeon_start"
class ExplorationApiDungeonGoalRequest(Request[ExplorationApiDungeonGoalResponse]):
    fieldStageMstId: int = None
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/dungeon_goal"
class ExplorationApiResetDungeonProgressRequest(Request[ExplorationApiResetDungeonProgressResponse]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/reset_dungeon_progress"
class ExplorationApiGetEnableStageListRequest(Request[ExplorationApiGetEnableStageListResponse]):
    @property
    def url(self) -> str:
        return "/api/exploration/get_enable_stage_list"
class ExplorationApiGetStageMstListRequest(Request[ExplorationApiGetStageMstListResponse]):
    fieldStageMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_stage_mst_list"
class ExplorationApiGetDungeonMstListRequest(Request[ExplorationApiGetDungeonMstListResponse]):
    dungeonMstId: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/get_dungeon_mst_list"
class ExplorationApiGetFieldStageCollectionInfoListRequest(Request[ExplorationApiGetFieldStageCollectionInfoListResponse]):
    @property
    def url(self) -> str:
        return "/api/exploration/get_field_stage_collection_info_list"
class ExplorationApiUpdateUserQuestMapEffectedDataRequest(Request[ExplorationApiUpdateUserQuestMapEffectedDataResponse]):
    questMapMstId: int = None
    difficulty: int = None
    @property
    def url(self) -> str:
        return "/api/exploration/update_user_quest_map_effected_data"
