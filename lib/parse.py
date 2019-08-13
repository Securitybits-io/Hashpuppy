#!/usr/bin/python3
import sys
import json
import requests
import codecs
import lib.list as list

def __readFile(filename):
    output = codecs.open(filename,'r', encoding='utf-8', errors='ignore').read().split('\n')
    return output

def __writeFile(filename, data):
    with open(filename, 'w') as file:
        for line in data:
            file.write('%s\n' % line)
    return

def __parsePWDump(input):
    output = []
    for line in input:
        if ":" in line:
            line = line.rstrip()
            output.append(line.split(':'))
        else:
            pass
    return output

def parse(url, token, username, id, input_path, output_path):
    file = __readFile(input_path)
    crackedCreds = __parsePWDump(list.get_all_cracked(url,token))
    credentials = []

    if(username):
        file = __parsePWDump(file)

    for line in file:
        i = 0
        for i in range(0,len(crackedCreds)):
            if(username):
                if line[id] == crackedCreds[i][0]:
                    credentials.append('{}:{}:{}'.format(line[0],crackedCreds[i][0],crackedCreds[i][1]))
                    # print('{}:{}:{}'.format(line[0],crackedCreds[i][0],crackedCreds[i][1]))
            else:
                if line == crackedCreds[i][0]:
                    credentials.append('{}:{}'.format(crackedCreds[i][0],crackedCreds[i][1]))
                    #print("{}:{}".format(crackedCreds[i][0],crackedCreds[i][1]))

    if(output_path == None):
        for line in credentials:
            print(line)
    else:
        __writeFile(output_path, credentials)

    return
