import configparser
from pathlib import Path

ini = Path("config.ini")
if not ini.is_file():
    config = configparser.ConfigParser()
    config['DEFAULT']={'windowsposition':'200x60-0-50'}
    config['scale']= {}
    config['scale']=  { 'ip':'192.168.10.200,192.168.10.201,192.168.10.202', # comma for mutiple ips
                        'port':'1749'}
                   
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

conf = configparser.ConfigParser()
conf.read('config.ini')
ips = list(conf['scale']['ip'].split(','))
port =int(conf['scale']['port'])
windowsposition = conf['DEFAULT']['windowsposition']