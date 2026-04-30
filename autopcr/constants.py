import os
from distutils.util import strtobool
import logging

SERVER_PORT = int(os.getenv("AUTOPCR_SERVER_PORT", "13200"))

PROXIES = {}

CLIENT_POOL_SIZE_MAX = 100
CLIENT_POOL_MAX_AGE = 3600 * 24
CLIENT_POOL_MAX_CLIENT_ALIVE = 10
SESSION_ERROR_MAX_RETRY = 2

API_LIMIT_TIMES = 5
API_LIMIT_INTERVAL = 1
LOGIN_LIMIT_TIMES = 5
LOGIN_LIMIT_INTERVAL = 30

BSDK = '日服'
QSDK = '国际服'
BSDKRSA = '日服（RSA登录）'
QSDKRSA = '国际服（RSA登录）'
SONET = '台服'

CHANNEL_OPTION = [BSDK, QSDK, BSDKRSA, QSDKRSA, SONET]

DEBUG_LOG = strtobool(os.getenv("AUTOPCR_SERVER_DEBUG_LOG", "false"))

ALLOW_REGISTER = strtobool(os.getenv("AUTOPCR_SERVER_ALLOW_REGISTER", 'true'))
SUPERUSER = str(os.getenv("AUTOPCR_SERVER_SUPERUSER", ""))

ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
CACHE_DIR = os.path.join(ROOT_DIR, './cache/')
RESULT_DIR = os.path.join(ROOT_DIR, './result/')
DATA_DIR = os.path.join(ROOT_DIR, './data/')
CONFIG_PATH = os.path.join(CACHE_DIR, './http_server/') 
OLD_CONFIG_PATH = os.path.join(ROOT_DIR, 'autopcr/http_server/config')
CLAN_BATTLE_FORBID_PATH = os.path.join(CONFIG_PATH, 'clan_battle_forbidden.txt')

LOG_PATH = os.path.join(ROOT_DIR, 'log/')
LOG_LEVEL = logging.INFO

# Headers
DEFAULT_HEADERS = {
  "content-type": "application/x-msgpack",
  "x-timezone-offset": "28800",
  "x-language": "ja-Jpan",
  "x-unity-version": "2022.3.21f1",
  "x-region": "JP",
  "user-agent": "UnityRequest   (Asus ASUS_I003DD Android OS 9 / API-28 (PI/rel.cjw.20220518.114133))"
}

IOS_HEADERS = {
}

from datetime import timezone, timedelta
USER_TZ = timezone(timedelta(hours=8))
