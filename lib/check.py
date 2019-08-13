#!/usr/bin/env python3
import json
import requests

def __data_conn():
    data_conn = {
        "section":"test",
        "request":"connection"
        }
    return data_conn

def __data_access(token):
    data_access = {
        "section": "test",
        "request": "access",
        "accessKey": token
        }
    return data_access

def __headers():
    headers = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
        }
    return headers

def Connection(url):
    connection = requests.post(url+"/user.php",
                               json=__data_conn(),
                               headers=__headers()
                               )
    response_code = connection.status_code
    return response_code

def Auth(url, token):
    status_code = Connection(url)

    if (status_code == 200):
        auth = requests.post(url+"/user.php",
                             json=__data_access(token),
                             headers=__headers()
                             )
        if auth.json()['response'] == 'OK':
            return True
        else:
            print('Unable to authenticate: %s' % auth.json()['message'])
            return False
    else:
        print('Could not contact server. Status Code: %s' % str(status_code))

    return False
