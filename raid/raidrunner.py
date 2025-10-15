import json
from .raidworker import raidworker
from typing import List, Tuple
from autopcr.db.database import db
from autopcr.model.models import *
import asyncio
from autopcr.core.sdkclient import region
from autopcr.sdk.sdkclients import bsdkclient, qsdkclient

with open('raid_config.json', 'r', encoding='utf-8') as fp:
    cfg = json.load(fp)

monitor: List[raidworker] = []
worker: Dict[region, List[raidworker]] = {}

def log(x: str):
    print(x)

def create_client(obj) -> raidworker:
    r = region(obj['region'])
    ret = raidworker(
        obj['code'],
        obj['password'],
        obj['alias'],
        bsdkclient if r == region.Japan else qsdkclient
    )
    ret.logger = log
    return ret

for item in cfg['monitor']:
    monitor.append(create_client(item))
for item in cfg['worker']:
    r = region(item['region'])
    if r not in worker:
        worker[r] = []
    worker[r].append(create_client(item))

stamina_cost = {}

async def prepare_all():
    global stamina_cost
    await asyncio.gather(*[m.prepare() for m in monitor + sum(worker.values(), [])])
    stamina_cost = {
        stage.multiRaidStageMstId: stage.useStaminaForRescue
        for stage in await db.mst(MstApiGetMultiRaidStageMstListRequest())
    }

worker_lock = {
    c: asyncio.Lock() for c in sum(worker.values(), [])
}

worker_index_dict: Dict[region, int] = {}

async def rescue(stageData: MultiRaidMultiRaidStageDataRecord, shouldRetry: bool, region: region):
    retry = len(worker[region])
    while retry > 0:
        cli = worker[region][worker_index_dict.get(region, 0)]
        worker_index_dict[region] = (worker_index_dict[region] + 1) % len(worker[region])
        retry -= 1
        async with worker_lock[cli]:
            if await cli.now_stamina() >= stamina_cost[stageData.multiRaidStageMstId]:
                try:
                    await cli.add_damage(stageData, stageData.hp)
                    log(f"[{cli.alias}] Rescued raid {stageData.multiRaidStageDataId} (Stage {stageData.multiRaidStageMstId}) with {stageData.hp} damage")
                    return
                except Exception as ex:
                    log(f"[{cli.alias}] Failed to rescue raid {stageData.multiRaidStageDataId}: {ex}")
                    if not shouldRetry: return

from datetime import datetime, timedelta, timezone

user_tz = timezone(timedelta(hours=8))

once_queue_dict: dict[region, List[MultiRaidMultiRaidStageDataRecord]] = {}

def get_once_queue(region: region) -> List[MultiRaidMultiRaidStageDataRecord]:
    global once_queue_dict
    if region not in once_queue_dict:
        once_queue_dict[region] = []
    return once_queue_dict[region]

def queue_raid(raid: MultiRaidMultiRaidStageDataRecord, region: region):
    once_queue = get_once_queue(region)
    if not any(r.multiRaidStageDataId == raid.multiRaidStageDataId for r in once_queue):
        once_queue.append(raid)

async def once_routine(region: region):
    once_queue = get_once_queue(region)
    while True:
        try:
            now_time = datetime.now(user_tz)
            log(f"Once routine checking for once raids...")
            to_rescue = []
            new_queue = []
            for stage in once_queue:
                if stage.hp <= 0:
                    continue
                raid_time = datetime.fromisoformat(stage.createdTime)
                threshold = now_time - timedelta(minutes=150)
                raid_time_user_tz = raid_time.astimezone(user_tz)
                if raid_time_user_tz > threshold:
                    log(f"Once routine Skipping raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) created at {raid_time_user_tz} (less than 10 minutes old)")
                    new_queue.append(stage)
                    continue
                log(f"Once routine Found raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) with {stage.hp}? HP")
                to_rescue.append(rescue(stage, False, region))
            once_queue.clear()
            once_queue.extend(new_queue)
            
            await asyncio.gather(*to_rescue)
        except Exception as ex:
            log(f"Once routine Monitoring failed: {ex}")
        await asyncio.sleep(60 * 5)

async def monitor_routine(monitor: raidworker):
    while True:
        try:
            now_time = datetime.now(user_tz)
            log(f"[{monitor.alias}] Checking for raids...")
            stages = await monitor.do_monitor()
            to_rescue = []
            for stage in stages:
                if stage.hp <= 0:
                    continue
                raid_time = datetime.fromisoformat(stage.createdTime)
                threshold = now_time - timedelta(minutes=10)
                raid_time_user_tz = raid_time.astimezone(user_tz)
                if raid_time_user_tz > threshold:
                    log(f"[{monitor.alias}] Skipping raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) created at {raid_time_user_tz} (less than 10 minutes old)")
                    continue
                log(f"[{monitor.alias}] Found raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) with {stage.hp} HP")
                to_rescue.append(rescue(stage, True, monitor.client.session.sdk.region))
            await asyncio.gather(*to_rescue)
        except Exception as ex:
            log(f"[{monitor.alias}] Monitoring failed: {ex}")
        await asyncio.sleep(60 * 5)

async def main():
    await prepare_all()
    await asyncio.gather(*(
        [monitor_routine(m) for m in monitor] + 
        [once_routine(region.Japan), once_routine(region.Global)]
        )
    )
