from pycomm3 import CIPDriver
devices = CIPDriver.discover() 

print(devices)