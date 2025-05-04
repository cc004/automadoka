from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timedelta, timezone

@description('溢出币自动兑换AQ币')
@name('购买金币')
@default(True)
class shop(Module):

    async def do_task(self, client: pcrclient):
        
        user_items = (await client.request(ItemApiGetItemDataListRequest())).itemDataList
        shop = await client.request(ShopApiGetShopListRequest())
        shop_mst = await db.mst(MstApiGetShopMstListRequest())
        shop_series_mst = await db.mst(MstApiGetShopSeriesMstListRequest())
        
        now = datetime.now(timezone.utc).astimezone()
        
        for mst in shop_series_mst:
            if datetime.fromisoformat(mst.startTime) > now or datetime.fromisoformat(mst.endTime) < now:
                continue
            if mst.category != 3:
                continue
            series = mst.shopSeriesMstId
            all_items = [s for s in shop_mst if s.shopGroupId in (mst.shopGroupId1, mst.shopGroupId2)]
            purchased = {
                s.shopMstId: s for s in shop.shopCountDataList if s.shopSeriesMstId == series
            }
            non_limited = [i for i in all_items if i.purchaseLimitCount == 0]
            if any(
                i.purchaseLimitCount != 0 and (
                    i.shopMstId not in purchased or
                    purchased[i.shopMstId].purchaseCount != i.purchaseLimitCount
                )
                for i in all_items
            ):
                self._log(f"商店{mst.title}含有未购买的限购物品，跳过")
                continue
            if len(non_limited) != 1:
                self._log(f"商店{mst.title}含有多于一个非限购物品，跳过")
                continue
            item_mst = non_limited[0]
            coin_cnt = sum(i.num for i in user_items if i.itemMstId == mst.payId)
            buy_num = coin_cnt // item_mst.price
            if buy_num <= 0:
                self._log(f"商店{mst.title}没有足够的金币，跳过")
                continue
            req_buy = ShopApiBuyRequest()
            req_buy.num = buy_num
            req_buy.shopMstId = item_mst.shopMstId
            req_buy.shopSeriesMstId = series
            await client.request(req_buy)
            self._log(f"购买商店{mst.title}的{item_mst.name}，数量：{buy_num}")
