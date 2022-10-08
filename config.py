import configparser
from pathlib import Path

ini = Path("config.ini")
if not ini.is_file():
    config = configparser.ConfigParser()
    config['scale']= {}
    config['scale']=  { 'ip':'192.168.10.200,192.168.10.201,192.168.10.202', # comma for mutiple ips
                        'port':'1749'}
                   
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config = configparser.ConfigParser()
config.sections()

config.read('config.ini')

scale = config['scale']
port = scale['port']

ips = []
for ip in scale['ip'].split(','):
    ips += [ip]
pass

for ip in ips:
    print (ip)
pass