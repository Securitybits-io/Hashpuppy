#!/usr/bin/python3
import json
import config
import requests

data_conn = {
    "section":"test",
    "request":"connection"
}

data_access = {
    "section": "test",
    "request": "access",
    "accessKey": config.token
}

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
req_conn = requests.post(config.url+"/user.php", json=data_conn, headers=headers)

print("HTTP Response Code: %s" % req_conn.status_code)
print(json.dumps(req_conn.json(), indent=4))

if req_conn.status_code == 200:
    print('Successful connect, Testing API Token')
    req_access = requests.post(config.url+"/user.php", json=data_access, headers=headers)
    print("HTTP Response Code: %s" % req_access.status_code)
    print(json.dumps(req_access.json(), indent=4))
