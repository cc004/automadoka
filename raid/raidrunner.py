import json
from .raidworker import raidworker
from typing import List, Tuple
from autopcr.db.database import db
from autopcr.model.models import *
import asyncio
from autopcr.core.sdkclient import region
from autopcr.sdk.sdkclients import bsdkclient, qsdkclient
from autopcr.core import pcrclient

with open('raid_config.json', 'r', encoding='utf-8') as fp:
    cfg = json.load(fp)

monitor: List[raidworker] = []
worker: Dict[region, List[raidworker]] = {}

def log(x: str):
    print(x)

def create_client(obj) -> raidworker:
    r = region[obj['region']]
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
    r = region[item['region']]
    if r not in worker:
        worker[r] = []
    worker[r].append(create_client(item))

backup_id = 0

async def backupLoaderJp() -> raidworker:
    global backup_id
    with open('backup_accounts.json', 'r', encoding='utf-8') as fp:
        backup_cfg: List[str] = json.load(fp)
    next_backup = backup_cfg[backup_id]
    backup_id = (backup_id + 1) % len(backup_cfg)
    
    code, password = next_backup.split(',')
    backup_worker = raidworker(
        code,
        password,
        'Backup JP Loader',
        bsdkclient
    )

    try:
        await backup_worker.prepare()
        lvl = backup_worker.client.data.resp.userParamData.level
        log(f"[Backup JP Loader] Logged in successfully. user level = {lvl}")
        if lvl > 50:
            log("[Backup JP Loader] User level too high, trying next backup account...")
            raise Exception("User level too high")
        return backup_worker
    except Exception as ex:
        log(f"[Backup JP Loader] Failed to log in: {ex}")
        with open('backup_accounts.json', 'w', encoding='utf-8') as fp:
            json.dump(
                backup_cfg[:backup_id] + backup_cfg[backup_id + 1 :] + [next_backup]
                ,fp, indent=4, ensure_ascii=False
            )
        
        return await backupLoaderJp()

backup_loader = {
    region.Japan: backupLoaderJp
}

async def prepare_progress(worker: raidworker):
    client = worker.client

    stratum = await db.mst(MstApiGetFieldStratumMstListRequest())
    point = await db.mst(MstApiGetFieldPointMstListRequest())
    field_mst = {
        x.fieldStageMstId: x for x in await db.mst(MstApiGetFieldStageMstListRequest())
    }

    top = await client.request(ExplorationApiGetFieldStageCollectionInfoListRequest())
    cleared_field = set(x.fieldStageMstId for x in top.fieldStageCollectionInfoList if x.isClear)

    def log(x: str):
        print(f"[{worker.alias}] {x}")

    async def clear_field(field: int):
        mst = field_mst[field]
        if field in cleared_field:
            log(f"跳过已通关篇章 {field} ({mst.name})")
            return
        if mst.prevFieldStageMstId != 0:
            await clear_field(mst.prevFieldStageMstId)
        log(f"开始清理 {field} ({mst.name})")
        top = await client.request(ExplorationApiGetTopInfoV4Request(
            fieldStageMstId=field
        ))
    
        if top.fieldStageUserData.clearFieldPointMstIdCsv:
            cleared_points = set(int(x) for x in top.fieldStageUserData.clearFieldPointMstIdCsv.split(','))
        else:
            cleared_points = set()
        
        stratums = [x for x in stratum if x.fieldStageMstId == field]

        for s in stratums:
            points = [x for x in point if x.fieldStratumMstId == s.fieldStratumMstId]
            for p in points:
                if p.fieldPointMstId in cleared_points:
                    log(f"跳过已通关点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                    continue
                reach = await client.request(ExplorationApiReachFieldPointRequest(
                    fieldPointMstId=p.fieldPointMstId
                ))
                log(f"到达点 {p.fieldPointMstId} ({mst.name}-{p.name})")

                if p.pointType == 1: # dungeon
                    start = await client.request(ExplorationApiDungeonStartRequest(
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonMstId=p.pointValue1
                    ))
                    finish = await client.request(ExplorationApiDungeonGoalRequest(
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonMstId=p.pointValue1
                    ))
                    log(f"完成副本点 {p.fieldPointMstId} ({mst.name}-{p.name})")
                elif p.pointType == 2 or p.pointType == 3 or p.pointType == 4: # start
                    quest = await client.request(ExplorationBattleApiInitializeStageV4Request(
                        fieldPointMstId=p.fieldPointMstId,
                        fieldStageMstId=s.fieldStageMstId,
                        dungeonEventMstId=0,
                        dungeonRoomMstId=0,
                        bossDirectionMstId=0,
                        presetEventIndex=0,
                        partyDataId=1
                    ))
                    await asyncio.sleep(2)
                    finish = await client.request(ExplorationBattleApiFinalizeStageForUserV4Request(
                        autoMode=1,
                        battleLog="",
                        result=1
                    ))
                    log(f"完成战斗点 {p.fieldPointMstId} ({mst.name}-{p.name})")

    await clear_field(605001)

async def prepare_or_backup(worker: raidworker):
    try:
        await worker.prepare()
    except Exception as ex:
        log(f"[{worker.alias}] Preparation failed: {ex}. Attempting to use backup loader...")
        if worker.client.session.sdk.region in backup_loader:
            backup_func = backup_loader[worker.client.session.sdk.region]
            backup_worker = await backup_func()
            worker.client = backup_worker.client
            worker.prepared = True
            log(f"[{worker.alias}] Backup loader assigned.")
        else:
            log(f"[{worker.alias}] No backup loader available for region {worker.client.session.sdk.region}.")
            raise ex
    finally:
        await prepare_progress(worker)

async def prepare_all():
    await asyncio.gather(*(
        [m.prepare() for m in monitor] + 
        [prepare_or_backup(w) for w in sum(worker.values(), [])]
    ))

worker_lock = {
    c: asyncio.Lock() for c in sum(worker.values(), [])
}

worker_index_dict: Dict[region, int] = {}

async def rescue(stageData: MultiRaidMultiRaidStageDataRecord, shouldRetry: bool, region: region):
    stamina_cost = {
        stage.multiRaidStageMstId: stage.useStaminaForRescue
        for stage in await db.mst(MstApiGetMultiRaidStageMstListRequest())
    }
    retry = len(worker[region])
    while retry > 0:
        if region not in worker_index_dict:
            worker_index_dict[region] = 0
        cli = worker[region][worker_index_dict[region]]
        worker_index_dict[region] = (worker_index_dict[region] + 1) % len(worker[region])
        retry -= 1
        async with worker_lock[cli]:
            log(f"[{cli.alias}] Attempting to rescue raid {stageData.multiRaidStageDataId} (Stage {stageData.multiRaidStageMstId}) with {stageData.hp} HP")
            if await cli.now_stamina() >= stamina_cost[stageData.multiRaidStageMstId]:
                try:
                    await cli.add_damage(stageData, stageData.hp)
                    log(f"[{cli.alias}] Rescued raid {stageData.multiRaidStageDataId} (Stage {stageData.multiRaidStageMstId}) with {stageData.hp} damage")
                    return
                except Exception as ex:
                    log(f"[{cli.alias}] Failed to rescue raid {stageData.multiRaidStageDataId}: {ex}")
                    if not shouldRetry: return

from datetime import datetime, timedelta, timezone
from autopcr.constants import USER_TZ as user_tz

once_queue_dict: Dict[region, List[MultiRaidMultiRaidStageDataRecord]] = {}

def get_once_queue(region: region) -> List[MultiRaidMultiRaidStageDataRecord]:
    global once_queue_dict
    if region not in once_queue_dict:
        once_queue_dict[region] = []
    return once_queue_dict[region]

def queue_raid(raid: MultiRaidMultiRaidStageDataRecord, region: region):
    once_queue = get_once_queue(region)
    if not any(r.multiRaidStageDataId == raid.multiRaidStageDataId for r in once_queue):
        once_queue.append(raid)

async def queue_raid_search(rid: str, region: region):
    client = worker[region][0].client
    try:
        resp = await client.request(MultiRaidApiIdSearchRequest(searchId=rid))
        if not resp.multiRaidStageDataList:
            log(f"[{region.value}] No raid found for ID {rid}")
            raise Exception("没有找到对应的raid")
        queue_raid(resp.multiRaidStageDataList[0], region)
    except Exception as ex:
        log(f"[{region.value}] Failed to search for raid {rid}: {ex}")
        raise

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
                #raid_time = datetime.fromisoformat(stage.createdTime)
                #threshold = now_time - timedelta(minutes=150)
                #raid_time_user_tz = raid_time.astimezone(user_tz)
                #if raid_time_user_tz > threshold:
                #    log(f"Once routine Skipping raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) created at {raid_time_user_tz} (less than 150 minutes old)")
                #    new_queue.append(stage)
                #    continue
                log(f"Once routine Found raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) with {stage.hp}? HP")
                to_rescue.append(rescue(stage, False, region))
            once_queue.clear()
            once_queue.extend(new_queue)
            
            await asyncio.gather(*to_rescue)
        except Exception as ex:
            log(f"Once routine Monitoring failed: {ex}")
            import traceback
            log(traceback.format_exc())
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
                #raid_time = datetime.fromisoformat(stage.createdTime)
                #threshold = now_time - timedelta(minutes=30)
                #raid_time_user_tz = raid_time.astimezone(user_tz)
                #if raid_time_user_tz > threshold:
                #    log(f"[{monitor.alias}] Skipping raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) created at {raid_time_user_tz} (less than 30 minutes old)")
                #    continue
                log(f"[{monitor.alias}] Found raid {stage.multiRaidStageDataId} (Stage {stage.multiRaidStageMstId}) with {stage.hp} HP")
                to_rescue.append(rescue(stage, True, monitor.client.session.sdk.region))
            await asyncio.gather(*to_rescue)
        except Exception as ex:
            log(f"[{monitor.alias}] Monitoring failed: {ex}")
            import traceback
            log(traceback.format_exc())
        await asyncio.sleep(60 * 5)

async def main():
    await prepare_all()
    await asyncio.gather(*(
        [monitor_routine(m) for m in monitor] + 
        [once_routine(region.Japan), once_routine(region.Global)]
        )
    )
