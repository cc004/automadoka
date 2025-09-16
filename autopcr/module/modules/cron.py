from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.error import *
from ...model.enums import *
from ...db.database import db

class CronModule(Module):
    def get_cron_time(self) -> str: ...

    async def is_cron_condition(self) -> bool: ...

    async def is_cron_time(self, nhour: int, nminute: int) -> bool:
        time_args = self.get_cron_time().split(":")
        hour, minute = time_args[0], time_args[1]
        return nhour == int(hour) and nminute == int(minute)

    async def update_client(self, client: pcrclient):
        client.set_cron_run()

    async def is_cron_run(self, hour: int, minute: int) -> bool:
        enable: bool = self.get_config(self.key)
        if enable and await self.is_cron_time(hour, minute) and await self.is_cron_condition():
            return True
        else:
            return False
    
    def judge_module_run(self, module: type) -> bool:
        return True

from .raid import support_raid

class NormalCronModule(CronModule):
    async def is_cron_condition(self) -> bool:
        return True

class SupportCronModule(CronModule):
    async def is_cron_condition(self) -> bool:
        return True
    def judge_module_run(self, module: type) -> bool:
        return module == support_raid


@timetype("time_cron1", "执行时间", "05:00")
@description('定时执行')
@name("定时任务1")
@default(False)
@notrunnable
class cron1(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron1")

@timetype("time_cron2", "执行时间", "09:00")
@description('定时执行')
@name("定时任务2")
@default(False)
@notrunnable
class cron2(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron2")


@timetype("time_cron3", "执行时间", "13:00")
@description('定时执行')
@name("定时任务3")
@default(False)
@notrunnable
class cron3(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron3")

@timetype("time_cron4", "执行时间", "17:00")
@description('定时执行')
@name("定时任务4")
@default(False)
@notrunnable
class cron4(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron4")

@timetype("time_cron5", "执行时间", "21:00")
@description('定时执行')
@name("定时任务5")
@default(False)
@notrunnable
class cron5(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron5")

@timetype("time_cron6", "执行时间", "01:00")
@description('定时执行')
@name("定时任务6")
@default(False)
@notrunnable
class cron6(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron6")

@timetype("time_cron1_", "执行时间", "05:05")
@description('定时执行')
@name("定时任务1（仅执行支援）")
@default(False)
@notrunnable
class cron1_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron1_")

@timetype("time_cron2_", "执行时间", "09:05")
@description('定时执行')
@name("定时任务2（仅执行支援）")
@default(False)
@notrunnable
class cron2_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron2_")


@timetype("time_cron3_", "执行时间", "13:05")
@description('定时执行')
@name("定时任务3（仅执行支援）")
@default(False)
@notrunnable
class cron3_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron3_")

@timetype("time_cron4_", "执行时间", "17:05")
@description('定时执行')
@name("定时任务4（仅执行支援）")
@default(False)
@notrunnable
class cron4_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron4_")

@timetype("time_cron5_", "执行时间", "21:05")
@description('定时执行')
@name("定时任务5（仅执行支援）")
@default(False)
@notrunnable
class cron5_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron5_")

@timetype("time_cron6_", "执行时间", "01:05")
@description('定时执行')
@name("定时任务6（仅执行支援）")
@default(False)
@notrunnable
class cron6_(SupportCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron6_")
