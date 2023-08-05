import json

import os
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

qloaded = {}

def qLoad(s: str):
    if s in qloaded:
        return qloaded[s]
    else:
        f = open(f"{ROOT_DIR}/{s}.txt", "r")
        t = json.loads(f.read())
        f.close()
        qloaded[s] = t
        return t
