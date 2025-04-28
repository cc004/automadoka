from typing import List, Dict, Set, Tuple, Union
import typing
import datetime
from collections import Counter, defaultdict
from .dbmgr import dbmgr
from .models import *
from ..util.linq import flow
from queue import SimpleQueue
from ..core.apiclient import apiclient
from typing import TypeVar, Generic

T = TypeVar("T")

class lazy_property(Generic[T]):
    def __init__(self, func):
        self.func = func
        self.attr_name = f"__cached_{func.__name__}"
        self.version_attr = f"__cached_version_{func.__name__}"
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self # type: ignore

        dbmgr = getattr(instance, "dbmgr", None)
        if dbmgr is None:
            raise ValueError("数据库未初始化完成，请稍等片刻")
        current_version = dbmgr.ver
        cached = getattr(instance, self.attr_name, None)
        cached_version = getattr(instance, self.version_attr, None)

        if cached is None or current_version != cached_version:
            value = self.func(instance)  # 现在函数里自己处理 db
            setattr(instance, self.attr_name, value)
            setattr(instance, self.version_attr, current_version)
            return value

        return cached

class database():
    def update(self, dbmgr):
        self.dbmgr = dbmgr
    
    def is_clan_battle_time(self): return False

    def format_time(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d %H:%M:%S")

    def format_date(self, time: datetime.datetime) -> str:
        return time.strftime("%Y/%m/%d")

    def format_time_safe(self, time: datetime.datetime) -> str:
        return time.strftime("%Y%m%d%H%M%S")

    def format_second(self, total_seconds: int) -> str:
        time_delta = datetime.timedelta(seconds=total_seconds)
        hours, remainder = divmod(time_delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"


db = database()
