#!/usr/bin/python3
import sys
import json
import config
import requests
import argparse
import base64

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def getHashlists(url, token):
    request_data = {
        "section":"hashlist",
        "request":"listHashlists",
        "accessKey":token
    }

    res_getHashlists = requests.post(url+"/user.php", json=request_data, headers=headers)
    response = res_getHashlists.json()
    hashlistId = []
    for hashlist in response['hashlists']:
        hashlistId.append(hashlist['hashlistId'])

    return hashlistId

def getCracked(url, token, hashlist):
    cracked = []
    for id in hashlist:
        request_data = {
            "section":"hashlist",
            "request":"getCracked",
            "hashlistId":id,
            "accessKey":config.token
            }
        res_cracked = requests.post(url+"/user.php", json=request_data, headers=headers)
        cracked.append(res_cracked.json()['cracked'])
    return cracked

def checkAuthentication(url, token):
    data_access = {
        "section": "test",
        "request": "access",
        "accessKey": token
    }

    res_access = requests.post(url+"/user.php", json=data_access, headers=headers)
    json_dict = res_access.json()

    return json_dict['response']

def exportHashes(hashes):
    crackedHashes = ""
    for list in hashes:
        for line in list:
            crackedHashes+= line['hash']+':'+line['plain']+'\n'
    return base64.b64encode(crackedHashes.encode('UTF-8'))[2:-1]

def importCracked(url, token, hashes, hashlistId):
    #data should be base64 encoded (UTF-8)
    for listId in hashlistId:
        request_data = {
            "section":"hashlist",
            "request":"importCracked",
            "hashlistId":listId,
            "separator":":",
            "data": '"'+str(hashes)+'"',
            "accessKey":token
            }

        res_import = requests.post(url+"/user.php", json=request_data, headers=headers)
        json_dict = res_import.json()
        if json_dict['response'] != 'ERROR':
            print('Importing cracked hashes for HashlistID: %s' % listId)
            print('Response: %s' % json_dict['response'])
            print('Lines Processed: %s' % json_dict['linesProcessed'])
            print('New Cracked: %s' % json_dict['newCracked'])
            print('Already Cracked: %s' % json_dict['alreadyCracked'])
            print('Invalid Lines: %s' % json_dict['invalidLines'])
            print('Process Time: %s \n' % json_dict['processTime'])
        else:
            print('Something Wong')
            print(json_dict)
    return

def main():
    parser = argparse.ArgumentParser(prog='./import_cracked.py', description='This script will extract all hashes and then import as "Cracked Hashes"\n updating all hashlists with newly cracked hashes')
    args = parser.parse_args()

    if checkAuthentication(config.url, config.token) == "OK":
        hashlistId = getHashlists(config.url, config.token)
        crackedHashes = getCracked(config.url, config.token, hashlistId)
        hashes = exportHashes(crackedHashes)
        print (hashes)
        importCracked(config.url, config.token, hashes, hashlistId)

    else:
        print('Authentication Failure, Check your API-Key')
        sys.exit()

if __name__ == "__main__":
    main()
