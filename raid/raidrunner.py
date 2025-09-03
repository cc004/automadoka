import json
from .raidworker import raidworker
from typing import List
from autopcr.db.database import db
from autopcr.model.models import *
import asyncio

with open('raid_config.json', 'r', encoding='utf-8') as fp:
    cfg = json.load(fp)

monitor: List[raidworker] = []
worker: List[raidworker] = []

def log(x: str):
    print(x)

def create_client(obj) -> raidworker:
    ret = raidworker(
        obj['code'],
        obj['password'],
        obj['alias']
    )
    ret.logger = log
    return ret

for item in cfg['monitor']:
    monitor.append(create_client(item))
for item in cfg['worker']:
    worker.append(create_client(item))

stamina_cost = {}

async def prepare_all():
    global stamina_cost
    await asyncio.gather(*[m.prepare() for m in monitor + worker])
    stamina_cost = {
        stage.multiRaidStageMstId: stage.useStaminaForRescue
        for stage in await db.mst(MstApiGetMultiRaidStageMstListRequest())
    }

worker_index = 0
worker_lock = {
    c: asyncio.Lock() for c in worker
}

async def rescue(stageData: MultiRaidMultiRaidStageDataRecord):
    global worker_index
    retry = len(worker)
    while retry > 0:
        cli = worker[worker_index]
        worker_index = (worker_index + 1) % len(worker)
        retry -= 1
        async with worker_lock[cli]:
            if await cli.now_stamina() >= stamina_cost[stageData.multiRaidStageMstId]:
                try:
                    await cli.add_damage(stageData, stageData.hp)
                    log(f"[{cli.alias}] Rescued raid {stageData.multiRaidStageDataId} (Stage {stageData.multiRaidStageMstId}) with {stageData.hp} damage")
                    return
                except Exception as ex:
                    log(f"[{cli.alias}] Failed to rescue raid {stageData.multiRaidStageDataId}: {ex}")
from datetime import datetime, timedelta, timezone

user_tz = timezone(timedelta(hours=8))

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
                to_rescue.append(rescue(stage))
            await asyncio.gather(*to_rescue)
        except Exception as ex:
            log(f"[{monitor.alias}] Monitoring failed: {ex}")
        await asyncio.sleep(60 * 5)

async def main():
    await prepare_all()
    await asyncio.gather(*[monitor_routine(m) for m in monitor])
