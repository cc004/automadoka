import os, json
from ..util.linq import flow
from ..constants import DATA_DIR
from collections import Counter
from typing import Dict, Counter as TCounter

def read_from(filename: str) -> object:
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
