import configparser

configparser = configparser.ConfigParser()

configparser.read('api.conf')

url=configparser['DEFAULT']['url']
token=configparser['DEFAULT']['token']
