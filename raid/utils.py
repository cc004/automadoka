from datetime import datetime, timedelta, timezone
from autopcr.model.models import MultiRaidMultiRaidConfig

user_tz = timezone(timedelta(hours=8))
def stamina_calc(current: int, update_time: str, config: MultiRaidMultiRaidConfig) -> int:
    now = datetime.now(tz=user_tz)
    update = datetime.fromisoformat(update_time).astimezone(user_tz)
    delta = now - update
    if delta.total_seconds() < 0 or current >= config.staminaUpperLimit:
        return current
    recover_times = delta.total_seconds() // config.staminaRecoverSec * config.staminaRecoverNum
    return min(current + int(recover_times), config.staminaUpperLimit)