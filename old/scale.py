import asyncio, telnetlib3
from glob import glob
import tkinter
# from program import app

async def output(reader):
    while True:
        outp = await reader.read(1024)
        print(outp, flush=True)
        return outp

async def shell1(reader, writer):
    i = '1'
    global weight1
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        weight1 = f'{i}{outp}'

async def shell2(reader, writer):
    i = '2'
    global weight2
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        weight2 = f'{i}{outp}'

async def shell3(reader, writer):
    i = '3'
    global weight3
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        weight3 = f'{i}{outp}'

async def shell_output():
    global total
    while True:
        await asyncio.sleep(0.5)
        try:
            total = int(weight1.split()[1]) + int(weight2.split()[1]) + int(weight3.split()[1])
            print(weight1)
            print(weight2)
            print(weight3)
            print(total)
        except NameError:
            continue
        
# loop = asyncio.get_event_loop()

# s1 = telnetlib3.open_connection('192.168.10.200', 1749, shell=shell1)
# s2 = telnetlib3.open_connection('192.168.10.201', 1749, shell=shell2)
# s3 = telnetlib3.open_connection('192.168.10.202', 1749, shell=shell3)

# reader, writer = loop.run_until_complete(s1)
# reader, writer = loop.run_until_complete(s2)
# reader, writer = loop.run_until_complete(s3)
# loop.run_until_complete(shell_output())

# loop.run_until_complete(writer.protocol.waiter_closed)