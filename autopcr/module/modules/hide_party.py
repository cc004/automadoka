"""隐藏队伍展示 —— 关闭排行榜里的队伍详情公开。

接口是 ``/api/user/save_option``。它是**整体替换**，所以这里先读回全量配置
再整体写回；具体的字段说明和坑见 :mod:`autopcr.util.useroption`。

这个模块存在的意义是给「总力战」收尾：结算记录里点进去就能看到出战队伍，
先把展示关掉再打。

总力战始终关闭，团战与打分各有一个开关。
"""

from ..config import *
from ..modulebase import *
from ...core.pcrclient import pcrclient
from ...core.apiclient import ApiException, NetworkException, VersionUpdatedException
from ...model.models import *

from ...util.useroption import build_option_payload


@name('隐藏队伍')
@default(False)
@booltype('hide_party_score_attack', '同时隐藏打分队伍', True)
@booltype('hide_party_multi_raid', '同时隐藏团战队伍', True)
@description('关闭总力战/团战/打分的队伍展示，别人就看不到你的出战队伍了')
class hide_party(Module):

    async def do_task(self, client: pcrclient):
        # 1) 读回当前设置（save_option 是整体替换，必须先拿到全量字段）
        try:
            current = await client.request(UserApiLoadOptionRequest())
        except VersionUpdatedException:
            raise SkipError("游戏协议刚刚更新完成，请重新运行本功能")
        except NetworkException:
            raise AbortError("网络异常，读取当前设置失败，请稍后重试")
        except ApiException as e:
            raise AbortError(f"读取当前设置失败：{e} (code={e.result_code})")

        data, changed = build_option_payload(
            current.dict(),
            hide_multi_raid=bool(self.get_config('hide_party_multi_raid')),
            hide_score_attack=bool(self.get_config('hide_party_score_attack')),
        )
        if not changed:
            self._log("队伍展示本来就是关闭的，无需修改")
            return

        # 2) 整体写回
        try:
            resp = await client.request(UserApiSaveOptionRequest(**data))
        except VersionUpdatedException:
            raise SkipError("游戏协议刚刚更新完成，请重新运行本功能")
        except NetworkException:
            raise AbortError("网络异常，保存设置失败，请稍后重试")
        except ApiException as e:
            raise AbortError(f"保存设置失败：{e} (code={e.result_code})")

        if not resp.isSuccess:
            raise AbortError("服务端拒绝了设置保存")

        self._log(f"已关闭队伍展示：{'、'.join(changed)}")
