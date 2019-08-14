#!/usr/bin/python3
import sys
import json
import requests
from pprint import *

def __headers():
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return headers

def __get_files(url, token):
    data_getfiles = {
        "section":"file",
        "request":"listFiles",
        "accessKey":token
    }

    files = requests.post(url+"/user.php", json=data_getfiles, headers=__headers())
    if files.status_code==200:
        return files.json()
    else:
        sys.exit()
    return

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

def __list_hashlists(url, token):
    data_listhashlist = {
        "section":"hashlist",
        "request":"listHashlists",
        "accessKey":token
    }
    hashlists = requests.post(url+"/user.php", json=data_listhashlist, headers=__headers())
    if hashlists.status_code == 200:
        return hashlists.json()
    else:
        sys.exit()
    return

def __get_hashlist(url, token, id):
    data_gethashlist = {
        "section" :"hashlist",
        "request": "getHashlist",
        "hashlistId": int(id),
        "accessKey": token
    }

    hashlist = requests.post(url+"/user.php", json=data_gethashlist, headers=__headers())
    if hashlist.status_code == 200:
        return hashlist.json()
    else:
        sys.exit()
    return

def get_all_cracked(url, token):
    cracked = []
    hashlists = __list_hashlists(url, token)

    for list in hashlists['hashlists']:
        list_cracked = __get_cracked(url, token, list['hashlistId'])
        for hash in list_cracked['cracked']:
            cracked.append(hash['hash']+':'+hash['plain'])
    return cracked

def print_files(url, token):
    files = __get_files(url, token)

    for file in files['files']:
        type = ""
        if file['fileType'] == 0:
            type = "dict"
        elif file['fileType'] == 1:
            type = "rule"
        elif file['fileType'] == 2:
            type = "file"

        print("Id: {:3} | Type: {:4} | Name: {}".format(file['fileId'], type, file['filename']))
    return

def print_cracked(url, token):
    cracked = get_all_cracked(url, token)
    for line in cracked:
        print('{}'.format(line))
    return

def print_hashlists(url, token):
    hashlists = __list_hashlists(url, token)
    for list in hashlists['hashlists']:
        hashlist = __get_hashlist(url,token,list['hashlistId'])
        print("Id: {:3} | hashtype: {:5} | Cracked: {:6}/{:<6} | Name: {} ".format(list['hashlistId'],list['hashtypeId'], hashlist['cracked'], list['hashCount'], list['name']))

    return
