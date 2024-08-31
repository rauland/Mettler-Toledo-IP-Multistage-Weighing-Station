"""Module parses config files"""
import configparser
from pathlib import Path

ini = Path("config.ini").resolve()
if not ini.is_file():
    config = configparser.ConfigParser()
    config['DEFAULT']={'windowsposition':'200x60-0-50'}
    config['scale'] = {}
    config['scale'] = { 'ip':'192.168.1.100,192.168.1.101,192.168.1.102', # comma delimiter for mutiple ips
                        'port':'1749'}
    with open(ini, 'w', encoding="utf-8") as configfile:
        config.write(configfile)

conf = configparser.ConfigParser()
conf.read(ini)
ips = list(conf['scale']['ip'].split(','))
port =int(conf['scale']['port'])
windowsposition = conf['DEFAULT']['windowsposition']
