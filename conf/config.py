import configparser

config = configparser.ConfigParser()

config.read('api.conf')

url=config['DEFAULT']['URL']
token=config['DEFAULT']['TOKEN']
