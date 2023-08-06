from cubizoid import common as c

def plugin(res):
  conf = res["functionConfig"]
  t = conf["spec"]["target"]
  res["items"] = [embed(conf, r) if c.isMatch(r, t) else r for r in res["items"]]
  return res

# Using the given config, a file will be embeded into the target
def embed(config, target):
  spec = config["spec"]
  file = spec["file"]
  contents = c.getFileContents(file)
  fileType = spec["fileType"] if "fileType" in spec else c.getMimeType(file)

  # nested means the file will be embedded as yaml into yaml
  if ("nested" in spec and spec["nested"]):
    contents = c.parseFrom(contents, fileType)

  # this will embed the file contents as the desired mime type
  elif ("parse" in spec):
    obj = c.parseFrom(contents, fileType)
    contents = c.parseTo(obj, spec["parse"])

  # apply the final patch to the resource
  return c.applyPatches(target, [{
    "op": "add",
    "path": spec["target"]["fieldPath"],
    "value": contents
  }])
