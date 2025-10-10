from ..modulebase import *
from ..config import *
from ...core.pcrclient import pcrclient
from ...model.models import *
from datetime import datetime, timezone

def item(category, item_mst_id, is_infinite):
    def wrapper(shop: ShopShopMstRecord):
        return shop.objectReceiveType == category and shop.objectId == item_mst_id and (shop.purchaseLimitCount == 0) == is_infinite
    return wrapper

def anyof(*conds):
    def wrapper(shop: ShopShopMstRecord):
        return any(cond(shop) for cond in conds)
    return wrapper

def it(id):
    return item(5, id, False)

item_category = {
    '肖像': lambda shop: shop.objectReceiveType == 4,
    '钥匙碎片': it(232030),
    '4x交换币': it(201017),
    '钻石': item(2, 0, False),
    '记忆切符': it(262001),
    '彩球': it(121003),
    '开孔材料': it(180001),
    '永久锁': it(180005),
    '技能书': anyof(
        it(123001), it(123002), it(123003)
    ),
    '新属性球': anyof(
        it(121023), it(121024), it(121025), it(121026), it(121027), it(121028)
    ),
    '属性球': anyof(
        it(121006), it(121009), it(121012), it(121015), it(121018), it(121021)
    ),
    'LP体力石': it(290001),
    '画板': anyof(
        it(122001), it(122002), it(122003)
    ),
    '体力石': it(202001),
    '心砂': anyof(
        it(113001), it(113002)
    ),
    '泪滴': it(180003),
    '经验': it(124001),
    '小石头': anyof(
        it(121001), it(121004), it(121007), it(121010), it(121013), it(121016), it(121019)
    ),
    '大石头': anyof(
        it(121002), it(121005), it(121008), it(121011), it(121014), it(121017), it(121020)
    ),
    '金币': item(11, 0, False),
    '经验（无限池）': item(5, 124001, True),
    '金币（无限池）': item(11, 0, True)
}

def shop_priority(cls):
    candidate = [i for i in range(0, 101)]
    priority = 100
    for key in item_category:
        cls = inttype(f'shop_priority_{key}', f'{key}优先级，越高越优先，0为不购买', priority, candidate)(cls)
        priority -= 3
    return cls

@description('按顺序兑换商店物品')
@shop_priority
@name('清空兑换币')
@default(True)
class shop(Module):
    async def do_task(self, client: pcrclient):
        user_items = (await client.request(ItemApiGetItemDataListRequest())).itemDataList
        item_keys = {item.itemMstId for item in user_items}
        user_items = {
            x: sum(i.num for i in user_items if i.itemMstId == x) for x in item_keys
        }
        shop = await client.request(ShopApiGetShopListRequest())
        shop_mst = await db.mst(MstApiGetShopMstListRequest())
        shop_series_mst = await db.mst(MstApiGetShopSeriesMstListRequest())
        
        item_dict = {
            x.itemMstId: x for x in await db.mst(MstApiGetItemMstListRequest())
        }

        def category_of(shop: ShopShopMstRecord):
            for key, cond in item_category.items():
                if cond(shop):
                    return key
            return "未知"

        def sort_key(shop: ShopShopMstRecord):
            for key, cond in item_category.items():
                if cond(shop):
                    priority = self.get_config(f'shop_priority_{key}')
                    rarity = item_dict[shop.objectId].rarity if shop.objectReceiveType == 5 and shop.objectId in item_dict else 0
                    efficiency = shop.num / shop.price if shop.price > 0 else 0
                    return (-priority, -rarity, -efficiency)

            raise AbortError(f"商店ID：{shop.shopMstId}，物品类别：{shop.objectReceiveType}，物品ID：{shop.objectId}")

        now = datetime.now(timezone.utc).astimezone()
        
        for mst in shop_series_mst:
            start = datetime.fromisoformat(mst.startTime)
            end = datetime.fromisoformat(mst.endTime)
            if (start > now or end < now) and end > start:
                continue
            if mst.category != 3:
                continue
            series = mst.shopSeriesMstId
            all_items = [s for s in shop_mst if s.shopGroupId in (mst.shopGroupId1, mst.shopGroupId2)]
            purchased = {
                s.shopMstId: s for s in shop.shopCountDataList if s.shopSeriesMstId == series
            }

            try:
                all_items.sort(key=sort_key)
            except AbortError as e:
                self._log(f"跳过商店{mst.title}，无法识别物品类别: {str(e)}")
                continue

            for item in all_items:
                start = datetime.fromisoformat(item.startTime)
                end = datetime.fromisoformat(item.endTime)
                if item.resetType == 1 and (
                     start > now or end < now
                ) and end > start:
                    continue
                category = category_of(item)
                if self.get_config(f'shop_priority_{category}') == 0:
                    self._log(f"商店{mst.title}的{item_name}类别{category}优先级为0，跳过")
                    continue
                bought = purchased[item.shopMstId].purchaseCount if item.shopMstId in purchased else 0
                item_name = item_dict[item.objectId].name if item.objectId in item_dict else category
                if item.purchaseLimitCount != 0 and bought >= item.purchaseLimitCount:
                    continue
                if item.price <= 0:
                    self._log(f"商店{mst.title}的{item_name}价格异常，跳过")
                    continue
                coin_cnt = user_items.get(mst.payId, 0)
                if coin_cnt < item.price:
                    self._log(f"商店{mst.title}的{item_name}金币不足，跳过")
                    break
                buy_num = coin_cnt // item.price
                if item.purchaseLimitCount != 0:
                    buy_num = min(buy_num, item.purchaseLimitCount - bought)

                req_buy = ShopApiBuyRequest()
                req_buy.num = buy_num
                req_buy.shopMstId = item.shopMstId
                req_buy.shopSeriesMstId = series
                await client.request(req_buy)
                self._log(f"购买商店{mst.title}的{item_name}[{item.price}]，数量：{buy_num}")
                user_items[mst.payId] = user_items.get(mst.payId, 0) - item.price * buy_num
