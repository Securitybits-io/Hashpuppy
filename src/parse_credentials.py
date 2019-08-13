#!/usr/bin/python3
import sys
import json
import config
import requests
import argparse
import codecs

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def readFile(filename):
    output = codecs.open(filename,'r', encoding='utf-8', errors='ignore').read().split('\n')
    return output

def writeFile(filename, data):
    with open(filename, 'w') as file:
        for line in data:
            file.write('%s\n' % line)
    return

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
    for line in hashes:
        print (line)
    return

def parsePWDump(input):
    output = []
    for line in input:
        if ":" in line:
            line = line.rstrip()
            output.append(line.split(':'))
        else:
            pass
    return output

def main():
    parser = argparse.ArgumentParser(prog='./parse_credentials.py')
    parser.add_argument('-i', '--input', type=str, help='Input credentials.txt to process', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file to write' )
    parser.add_argument('-p', '--position', type=int, help='Array position in file for hash', default=3, required=True)
    args = parser.parse_args()

    if checkAuthentication(config.url, config.token) == "OK":
        fileCreds = readFile(args.input)

        crackedCreds = []
        for line in parsePWDump(fileCreds):
            crackedHash = getHash(config.url, config.token, line[args.position])
            if crackedHash['response'] == 'OK':
                #print(line[1] + ':' + crackedHash['response'])
                crackedCreds.append(line[0] + ':'+line[args.position]+':'+crackedHash['plain'])
            else:
                pass

        if args.output == None:
            printHashes(crackedCreds)
        else:
            writeFile(args.output, crackedCreds)
    else:
        print('Authentication Failure, Check your API-Key')

if __name__ == "__main__":
    main()
