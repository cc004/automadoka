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

class NormalCronModule(CronModule):
    def get_clanbattle_run_status(self) -> bool: ...

    async def is_cron_condition(self) -> bool:
        is_clan_battle_run = self.get_clanbattle_run_status()
        is_clan_battle_time = db.is_clan_battle_time()
        return not is_clan_battle_time or is_clan_battle_run


@timetype("time_cron1", "执行时间", "05:00")
@booltype("clanbattle_run_cron1", "会战期间执行", False)
@description('定时执行')
@name("定时任务1")
@default(False)
@notrunnable
class cron1(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron1")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron1")

@timetype("time_cron2", "执行时间", "09:00")
@booltype("clanbattle_run_cron2", "会战期间执行", False)
@description('定时执行')
@name("定时任务2")
@default(False)
@notrunnable
class cron2(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron2")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron2")


@timetype("time_cron3", "执行时间", "13:00")
@booltype("clanbattle_run_cron3", "会战期间执行", False)
@description('定时执行')
@name("定时任务3")
@default(False)
@notrunnable
class cron3(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron3")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron3")

@timetype("time_cron4", "执行时间", "17:00")
@booltype("clanbattle_run_cron4", "会战期间执行", False)
@description('定时执行')
@name("定时任务4")
@default(False)
@notrunnable
class cron4(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron4")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron4")

@timetype("time_cron5", "执行时间", "21:00")
@booltype("clanbattle_run_cron5", "会战期间执行", False)
@description('定时执行')
@name("定时任务5")
@default(False)
@notrunnable
class cron5(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron5")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron5")

@timetype("time_cron6", "执行时间", "01:00")
@booltype("clanbattle_run_cron6", "会战期间执行", False)
@description('定时执行')
@name("定时任务6")
@default(False)
@notrunnable
class cron6(NormalCronModule):
    def get_cron_time(self) -> str:
        return self.get_config("time_cron6")
    def get_clanbattle_run_status(self) -> bool:
        return self.get_config("clanbattle_run_cron6")
