import json

import os
def popen(t, *args, **kwargs):
    return open(os.path.relpath(os.getcwd(), os.path.join(os.path.dirname(os.path.abspath(__file__)), t)), *args, **kwargs)

qloaded = {}

def qLoad(s: str):
    if s in qloaded:
        return qloaded[s]
    else:
        f = popen(f"{s}.txt", "r")
        t = json.loads(f.read())
        f.close()
        qloaded[s] = t
        return t
