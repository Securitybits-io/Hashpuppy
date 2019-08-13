#!/usr/bin/python3
import sys
import json
import config
import requests
import argparse


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def getHashlists(url, token, type):
    request_data = {
        "section":"hashlist",
        "request":"listHashlists",
        "accessKey":token
    }

    res_getHashlists = requests.post(config.url+"/user.php", json=request_data, headers=headers)
    response = res_getHashlists.json()
    hashlistId = []
    for hashlist in response['hashlists']:
        if str(hashlist['hashtypeId']) == type:
            hashlistId.append(hashlist['hashlistId'])
        elif str(type).upper() == 'ALL':
            hashlistId.append(hashlist['hashlistId'])
        else:
            print('Please specify an exisitng hashtype or ALL')
            print('Exiting...')
            sys.exit()

    return hashlistId

def getCracked(url, token, hashlist):
    cracked = []
    for id in hashlist:
        request_data = {
            "section":"hashlist",
            "request":"getCracked",
            "hashlistId":id,
            "accessKey":token
            }
        res_cracked = requests.post(config.url+"/user.php", json=request_data, headers=headers)
        cracked.append(res_cracked.json()['cracked'])
    return cracked


def checkAuthentication(url, token):
    data_access = {
        "section": "test",
        "request": "access",
        "accessKey": config.token
    }

    res_access = requests.post(config.url+"/user.php", json=data_access, headers=headers)
    json_dict = res_access.json()

    return json_dict['response']

def printHashes(hashes):
    for list in hashes:
        for line in list:
            print(line['hash']+':'+line['plain'])
    return

def main():
    parser = argparse.ArgumentParser(prog='./display_cracked.py', description='This script will list all cracked hash:pass to STDOUT')
    parser.add_argument('-i', type=str, help='Input specific hashcat Hash ID or ALL(Default)', default='ALL')
    args = parser.parse_args()

    if checkAuthentication(config.url, config.token) == "OK":
        hashlistId = getHashlists(config.url, config.token, args.i)
        crackedHashes = getCracked(config.url, config.token, hashlistId)
        printHashes(crackedHashes)
    else:
        print('Authentication Failure, Check your API-Key')

if __name__ == "__main__":
    main()
