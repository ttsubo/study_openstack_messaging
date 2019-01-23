import json
from httplib import HTTPConnection
from base64 import b64encode

url_path = "/api/queues/%2f/engine"
auth = "guest:guest"

header = {
    "Authorization" : "Basic %s" % b64encode(auth),
    "Content-Type": "application/json",
}

session = HTTPConnection("%s:%s" % ("127.0.0.1", 15672))
session.request("GET", url_path, "", header)
response =  session.getresponse()
ret = json.load(response)
print(json.dumps(ret, sort_keys=False, indent=4))
