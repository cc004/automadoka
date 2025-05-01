from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timedelta, timezone

@description('')
@name('领取登陆奖励')
@default(True)
class loginbonus(Module):
    async def do_task(self, client: pcrclient):
        req = HomeApiGetHomeInfoRequest()
        req.skipLoginBonus = False
        await client.request(req)


@description('')
@name('玩家信息')
@default(True)
class info(Module):
    async def do_task(self, client: pcrclient):
        self._log(f"用户名：{client.data.resp.userParamData.name} 等级: {client.data.resp.userParamData.level}")
        self._log(f"最高战力: {client.data.resp.userParamData.maxPartyPower} AQ: {client.data.resp.userParamData.money}")
