
import copy
import sys

from cubizoid import common as c

def plugin(res):
  config = res["functionConfig"]
  t = config["spec"]["target"]
  o = []
  if "template" in config["spec"]:
    o.extend(replicate(config), config["spec"]["template"])
  for r in res["items"]:
    if c.isMatch(r, t):
      o.extend(replicate(config, r))
    else:
      o.append(r)
  res["items"] = o
  return res

def replicate(plugin, output, res):
  c.mergeMeta(res, plugin)
  spec = plugin["spec"]
  items = spec["items"]
  itemsLen = len(items)
  if "replicas" not in spec:
    spec["replicas"] = itemsLen
  replicas = spec["replicas"]
  ttlIter = 1 # total amount of iterations through the item list
  itemIdx = 0 # the index of the current item for the iteration

  # iterate for the amount of replicas
  for i in range(replicas):

    # resetting item index  allows for more replicas than the count of items
    if itemIdx >= itemsLen:
      itemIdx = 0
      ttlIter += 1 # the count of how many times we have gone over the items
    
    # get the current item and a copy of the resource
    item = items[itemIdx]
    replicate = copy.deepcopy(res)

    # rename the replica to avoid conflicts
    if "rename" in spec:
      name = replicate["metadata"]["name"]
      prefix = ""
      suffix = ""
      if "prefix" in spec["rename"]:
        prefix = spec["rename"]["prefix"].format(i=i, iter=ttlIter, item=item)
      if "suffix" in spec["rename"]:
        suffix = spec["rename"]["suffix"].format(i=i, iter=ttlIter, item=item)
      replicate["metadata"]["name"] = "{0}{1}{2}".format(prefix, name, suffix)
    else:
      replicate["metadata"]["name"] += "-{0}-{1}".format(ttlIter, item)

    # the overrides make the differences between the replicas
    for ov in spec["overrides"]:
      if "target" not in ov or c.isMatch(replicate, ov["target"]):
        patches = []
        for patch in ov["patches"]:
          cpPatch = copy.deepcopy(patch)

          # resolve template value only if there is a string value key
          if "value" in patch and type(patch["value"]) == str:
              if patch["op"] == "add":
                cpPatch["value"] = patch["value"].format(i=i, iter=ttlIter, item=item)
              elif patch["op"] == "replace":
                v = c.deepGet(replicate, patch["path"])
                cpPatch["value"] = patch["value"].format(v, i=i, iter=ttlIter, item=item)
          patches.append(cpPatch)
        replicate = c.applyPatches(replicate, patches)
    output.append(replicate)
    # inc the iteration
    itemIdx += 1


