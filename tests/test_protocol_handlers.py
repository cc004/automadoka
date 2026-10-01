"""Business handlers must accept bundled models and existing generated caches."""
import asyncio
import unittest
from types import SimpleNamespace

from pydantic import BaseModel, Field

from autopcr.model import models, registry
from autopcr.model._bundled.common import FriendFriendMedal


class CachedFriendFriendMedal(BaseModel):
    type_: str = Field(None, alias='type')
    num: int = None


class LikeHandlerTests(unittest.TestCase):
    def test_friend_medal_alias_and_daily_limit(self):
        handler = registry._handlers['LikeApiExecLikeListResponse']
        response = models.LikeApiExecLikeListResponse.parse_obj({'resultList': [
            {'isFriendMedalAcquired': False},
            {'isFriendMedalAcquired': True},
            {'isFriendMedalAcquired': True},
        ]})
        for medal_class in (FriendFriendMedal, CachedFriendFriendMedal):
            with self.subTest(model=medal_class.__name__):
                medals = [medal_class.parse_obj(data) for data in (
                    {'type': 'Other', 'num': 999}, {'type': 'ExecLike', 'num': 10})]
                for limit, expected in ((100, 20), (15, 15)):
                    user = SimpleNamespace(todayFriendMedalCount=0)
                    manager = SimpleNamespace(
                        config=SimpleNamespace(friendConfig=SimpleNamespace(
                            friendMedal=medals, gainTodayFriendMedalMaxNum=limit)),
                        resp=SimpleNamespace(userParamData=user))
                    asyncio.run(handler(response, manager, None))
                    self.assertEqual(user.todayFriendMedalCount, expected)
