#!/usr/bin/python3
import sys
import json
import requests

def __headers():
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return headers

def __data_gethash(token, hash):

    return data_gethash

def __getHash(url, token, hash):
    __data_gethash = {
        "section": "hashlist",
        "request": "getHash",
        "hash": hash,
        "accessKey": token
    }

    res_gethash = requests.post(url+"/user.php",
                                json=__data_gethash,
                                headers=__headers())
    return res_gethash.json()

def __printHashes(hashes):
    print(hashes['hash']+':'+hashes['plain'])
    return

def search(url, token, hash):
    crackedHash = __getHash(url, token, hash)
    if crackedHash['response'] == 'OK':
        __printHashes(crackedHash)
    elif crackedHash['response'] == 'ERROR':
        print('ERROR: %s' % crackedHash['message'])
    else:
        print('ERROR: Exiting')
        sys.exit()
