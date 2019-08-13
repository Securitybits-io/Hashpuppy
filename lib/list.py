#!/usr/bin/python3
import sys
import json
import requests
from pprint import *

def __headers():
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return headers

def __get_cracked(url, token, id):
    data_getcracked = {
        "section":"hashlist",
        "request":"getCracked",
        "hashlistId":id,
        "accessKey":token
        }

    cracked = requests.post(url+"/user.php", json=data_getcracked, headers=__headers())
    if cracked.status_code == 200:
        return cracked.json()
    else:
        sys.exit()
    return

def __get_hashlist(url, token):
    data_gethashlist = {
        "section":"hashlist",
        "request":"listHashlists",
        "accessKey":token
    }
    hashlists = requests.post(url+"/user.php", json=data_gethashlist, headers=__headers())
    if hashlists.status_code == 200:
        return hashlists.json()
    else:
        sys.exit()
    return

def print_hashlists(url, token):
    hashlists = __get_hashlist(url, token)
    for list in hashlists['hashlists']:
        print("Id: {:3} | hashtype: {:5} | Hash Count: {:5} | Name: {} ".format(list['hashlistId'],list['hashtypeId'],list['hashCount'], list['name']))

    return
