#!/usr/bin/python3
import sys
import json
import requests
import base64
import codecs
import lib.list as list

def __headers():
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return headers

def __readFileB64(file):
    output = codecs.open(file,'r', encoding='utf-8', errors='ignore').read()#.split('\n')
    output = str(base64.b64encode(output.encode('utf-8')))
    return output

def importCracked(url, token, file, listId):
    hashes = __readFileB64(file)

    request_data = {
        "section":"hashlist",
        "request":"importCracked",
        "hashlistId":listId,
        "separator":":",
        "data": str(hashes)[2:-1],
        "accessKey":token
        }

    res_importCracked = requests.post(url+"/user.php", json=request_data, headers=__headers())
    json_dict = res_importCracked.json()
    if json_dict['response'] != 'ERROR':
        print('Importing cracked hashes for HashlistID: %s' % listId)
        print('Response: %s' % json_dict['response'])
        print('Lines Processed: %s' % json_dict['linesProcessed'])
        print('New Cracked: %s' % json_dict['newCracked'])
        print('Already Cracked: %s' % json_dict['alreadyCracked'])
        print('Invalid Lines: %s' % json_dict['invalidLines'])
        print('Process Time: %ssec' % json_dict['processTime'])
    else:
        print('Something Wong')
        print(json_dict)

    return
