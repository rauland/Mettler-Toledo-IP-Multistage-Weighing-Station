import configparser
from pathlib import Path
from turtle import position

ini = Path("config.ini")
if not ini.is_file():
    config = configparser.ConfigParser()
    config['DEFAULT']={'windowsposition':'200x60-0-50'}
    config['scale']= {}
    config['scale']=  { 'ip':'192.168.10.200,192.168.10.201,192.168.10.202', # comma for mutiple ips
                        'port':'1749'}
                   
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get():
    config = configparser.ConfigParser()
    # config.sections()
    config.read('config.ini')

    scale = config['scale']
    port = scale['port']
    ips = list(scale['ip'].split(','))

    return ips, port