from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *

@description('测试项目')
@name('测试')
@default(True)
class test(Module):
    async def do_task(self, client: pcrclient):
        req = HomeApiGetHomeInfoRequest()
        await client.request(req)
        raise SkipError('测试完毕')
