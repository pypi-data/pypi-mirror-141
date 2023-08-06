import sys
import os
import yaml
import re
import requests
from pathlib import Path
import json
import jsonpatch
import operator

def execute(plugin):
  dump(plugin(makeResourceList()))
  
def dump(res):
  if "config.kubernetes.io/function" in res["functionConfig"]["metadata"]["annotations"]:
    # print("Running krm function", file=sys.stderr)
    yaml.safe_dump(res, sys.stdout, default_flow_style=False);
  else:
    # print("Running legacy plugin", file=sys.stderr)
    yaml.safe_dump_all(res["items"], sys.stdout, default_flow_style=False);

def makeResourceList():
  # if pipeline
  if not sys.stdin.isatty():
    res = list(yaml.safe_load_all(sys.stdin))
  else:
    res = []

  # if a ResourceList was passed as stdin
  if len(res) == 1 and res[0]["kind"] == "ResourceList":
    res[0]["type"] = "krm"
    return res[0]
  else:
    f = sys.argv[-1]
    if not os.path.isfile(f):
      pluginFail("Could not load configuration: {}".format(f))
    conf = config(f)
    if "annotations" not in conf["metadata"]:
      conf["metadata"]["annotations"] = {}
    return {
      "kind": "ResourceList",
      "functionConfig": conf,
      "items": res,
      "type": "legacy"
    }


def config(file):
  try:
    c = getFileContents(file)
    y = yaml.safe_load(c)
  except yaml.YAMLError as exc:
    print("Error parsing input", file=sys.stderr)
    sys.exit(1)
  return y

def query(items, target):
  output = []
  for r in items:
    if isMatch(r, target):
      output.append(r)
  return output

def getFileContents(file):
  if file.startswith("http"):
    r = requests.get(file, allow_redirects=True)
    return r.content
  else:
    return Path(file).read_text()

def getMimeType(file):
  inferredType = Path(file).suffix
  # print("inferredType = "+inferredType)
  if inferredType in [".yaml", ".yml"]:
    return "yaml"
  elif inferredType == ".json":
    return "json"
  else:
    return "na"

def parseFrom(contents, mimeType = yaml):
  if mimeType == "yaml":
    return yaml.safe_load(contents)
  elif mimeType == "json":
    return json.loads(contents)
  else:
    pluginFail("Only json and yaml files may be parsed to objects")

def parseTo(obj, mimeType = "yaml"):
  if mimeType == "yaml":
    return yaml.safe_dump(obj)
  elif mimeType == "json":
    return json.dumps(obj)
  else:
    pluginFail("Objects may only be dumped to yaml or json")

def applyPatches(target, patches):
  p = jsonpatch.JsonPatch(patches)
  return p.apply(target)

def mergeMeta(res, plugin):
  if "name" not in res["metadata"]:
    res["metadata"]["name"] = plugin["metadata"]["name"]
  if "namespace" not in res["metadata"] and "namespace" in plugin["metadata"]:
    res["metadata"]["namespace"] = plugin["metadata"]["namespace"]
  if "labels" in plugin["metadata"]:
    if "labels" not in res["metadata"]:
      res["metadata"]["labels"] = {}
    res["metadata"]["labels"] = {**res["metadata"]["labels"], **plugin["metadata"]["labels"], }
  
  # currently merging the annotations will cause the resource to be ignored when using krm functions
  # this happens because the krm config has config.kubernetes.io/local-config: 'true'
  # if "annotations" in plugin["metadata"]:
  #   if "annotations" not in res["metadata"]:
  #     res["metadata"]["annotations"] = {}
  #   res["metadata"]["annotations"] = {**res["metadata"]["annotations"], **plugin["metadata"]["annotations"], }
  return res

def isMatch(res, target):

  # match apiVersion filter
  if "apiVersion" in target and not re.match(target["apiVersion"], res["apiVersion"]):
    return False

  # match by kind filter
  if "kind" in target and not re.match(target["kind"], res["kind"]):
    return False

  # match by name filter
  if "name" in target and not re.match(target["name"], res["metadata"]["name"]):
    return False

  # match by label selector
  if "matchLabels" in target:
    if not "labels" in res["metadata"]:
      return False
    labels = dict(res["metadata"]["labels"])
    if not dict(labels, **target["matchLabels"]) == labels:
      return False

  # match by annotations selector
  if "matchAnnotations" in target:
    if not "annotations" in res["metadata"]:
      return False
    annotations = dict(res["metadata"]["annotations"])
    if not dict(annotations, **target["matchAnnotations"]) == annotations:
      return False

  # if all checks passed or there were none at all
  return True

def pluginFail(message):
  print >> sys.stderr, message
  sys.exit(1)

_default_stub = object()
def deepGet(obj, path, default=_default_stub, separator='/'):
    """
    found here: https://codereview.stackexchange.com/questions/139810/python-deep-get
    Gets arbitrarily nested attribute or item value.

    Args:
        obj: Object to search in.
        path (str, hashable, iterable of hashables): Arbitrarily nested path in obj hierarchy.
        default: Default value. When provided it is returned if the path doesn't exist.
            Otherwise the call raises a LookupError.
        separator: String to split path by.

    Returns:
        Value at path.

    Raises:
        LookupError: If object at path doesn't exist.

    Examples:
        >>> deep_get({'a': 1}, 'a')
        1

        >>> deep_get({'a': 1}, 'b')
        Traceback (most recent call last):
            ...
        LookupError: {u'a': 1} has no element at 'b'

        >>> deep_get(['a', 'b', 'c'], -1)
        u'c'

        >>> deep_get({'a': [{'b': [1, 2, 3]}, 'some string']}, 'a.0.b')
        [1, 2, 3]

        >>> class A(object):
        ...     def __init__(self):
        ...         self.x = self
        ...         self.y = {'a': 10}
        ...
        >>> deep_get(A(), 'x.x.x.x.x.x.y.a')
        10

        >>> deep_get({'a.b': {'c': 1}}, 'a.b.c')
        Traceback (most recent call last):
            ...
        LookupError: {u'a.b': {u'c': 1}} has no element at 'a'

        >>> deep_get({'a.b': {'Привет': 1}}, ['a.b', 'Привет'])
        1

        >>> deep_get({'a.b': {'Привет': 1}}, 'a.b/Привет', separator='/')
        1

    """
    # split after first slash or char, 
    # this means the original string must always include an extra separator in the front
    attributes = path[1:].split(separator)

    LOOKUPS = [getattr, operator.getitem, lambda obj, i: obj[int(i)]]
    try:
        for i in attributes:
            # replace any jsonpath like escapes
            i = i.replace('~0', '~').replace('~1', "/")
            for lookup in LOOKUPS:
                try:
                    obj = lookup(obj, i)
                    break
                except (TypeError, AttributeError, IndexError, KeyError,
                        UnicodeEncodeError, ValueError):
                    pass
            else:
                msg = "{obj} has no element at '{i}'".format(obj=obj, i=i)
                raise LookupError(msg.encode('utf8'))
    except Exception:
        if _default_stub != default:
            print("Found default stub")
            return default
        raise
    return obj