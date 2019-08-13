#!/usr/bin/python3
import sys
import json
import config
import requests
import argparse

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
def getHash(url, token, hash):
    data_gethash = {
        "section": "hashlist",
        "request": "getHash",
        "hash": hash,
        "accessKey": token
    }

    res_gethash = requests.post(url+"/user.php", json=data_gethash, headers=headers)
    return res_gethash.json()

def checkAuthentication(url, token):
    data_access = {
        "section": "test",
        "request": "access",
        "accessKey": token
    }

    res_access = requests.post(url+"/user.php", json=data_access, headers=headers)
    json_dict = res_access.json()

    return json_dict['response']

def printHashes(hashes):
    print(hashes['hash']+':'+hashes['plain'])
    return

def main():
    parser = argparse.ArgumentParser(prog='./display_cracked.py')
    parser.add_argument('HASH', type=str, help='Input specific hash to lookup if cracked')
    args = parser.parse_args()

    if checkAuthentication(config.url, config.token) == "OK":

        crackedHash = getHash(config.url, config.token, args.HASH)
        if crackedHash['response'] == 'OK':
            printHashes(crackedHash)
        elif crackedHash['response'] == 'ERROR':
            print('ERROR: %s' % crackedHash['message'])
        else:
            print('ERROR: Exiting')
            sys.exit()
    else:
        print('Authentication Failure, Check your API-Key')

if __name__ == "__main__":
    main()
