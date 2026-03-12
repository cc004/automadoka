from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *

@description('自动抽取免费扭蛋')
@name('免费扭蛋')
@default(True)
class freegacha(Module):
    async def do_task(self, client: pcrclient):
        gacha_top = await client.request(GachaApiGetGachaTopRequest())
        free_gacha = [x for x in gacha_top.viewData.gachaList if x.price == 0]

        gacha_count = {
            x.gachaMstId: (x.dailyCount, x.totalCount)
            for x in gacha_top.viewData.gachaCountDataList
        }

        style_dict = {
            x.styleMstId: x
            for x in await db.mst(MstApiGetStyleMstListRequest())
        }
        char_dict = {
            x.characterMstId: x
            for x in await db.mst(MstApiGetCharacterMstListRequest())
        }

        def pretty_print(data: ObjectStyleGainViewData) -> str:
            style = style_dict[data.styleMstId]
            character = char_dict[data.styleMstId // 10000]
            rarity = int(style.rarity)
            sb = []
            sb.append(' ' * (5 - rarity))
            sb.append('*' * rarity)
            sb.append("    ")

            sb.append(f"[{style.name}] {character.name}")

            if data.isNew:
                sb.append(" new!")

            return ''.join(sb)

        for gacha in free_gacha:
            dailyCount, totalCount = gacha_count.get(gacha.gachaMstId, (0, 0))
            if gacha.countLimit != 0 and gacha.countLimit <= totalCount:
                self._log(f'{gacha.gachaName} 已经抽取过了，跳过')
            if gacha.dailyCountLimit != 0 and gacha.dailyCountLimit <= dailyCount:
                self._log(f'{gacha.gachaName} 今日抽取次数已满，跳过')

            request = GachaApiGachaExecRequest()
            request.gachaMstId = gacha.gachaMstId
            
            response = await client.request(request)
            self._log(f'抽取 {gacha.gachaName}，结果：')
            for data in response.objectDataRecord.gainViewData.styleGainViewDataList:
                self._log(pretty_print(data))
        
            