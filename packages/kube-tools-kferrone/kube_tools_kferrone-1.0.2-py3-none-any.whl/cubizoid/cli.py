
from cubizoid import common as c
import sys
from importlib import import_module

def main():
    # print(sys.argv, file=sys.stderr)
    res = c.makeResourceList()
    kind = res["functionConfig"]["kind"].lower()
    p = import_module("cubizoid.plugins.{}".format(kind))
    c.dump(p.plugin(res))
    