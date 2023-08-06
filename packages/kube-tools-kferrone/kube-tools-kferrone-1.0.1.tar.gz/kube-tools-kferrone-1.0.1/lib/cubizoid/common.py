import sys
import yaml
import re
import select

def execute(plugin):
  c = config()
  res = list(yaml.safe_load_all(sys.stdin))
  if len(res) > 0:
    o = plugin.transform(c, res);
  else:
    o = plugin.generate(c);
  yaml.safe_dump_all(o, sys.stdout, default_flow_style=False);

def config():
  with open(sys.argv[1], "r") as stream:
    try:
      c = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print("Error parsing input", file=sys.stderr)
      sys.exit(1)
  return c

def isMatch(res, target):

  # match by name filter
  if "name" in target and not re.match(target["name"], res["metadata"]["name"]):
    return False

  # match by kind filter
  if "kind" in target and not re.match(target["kind"], res["kind"]):
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