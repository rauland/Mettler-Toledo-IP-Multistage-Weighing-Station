import asyncio, telnetlib3
import tkinter
from program import app
asyncio.set_event_loop(asyncio.new_event_loop())

h1 = '192.168.10.200'
h2 = '192.168.10.201'
h3 = '192.168.10.202'

async def output(hostname):
    s = telnetlib3.open_connection(hostname, 1749)
    while True:
        outp = await s.reader.read(1024)
        print(outp, flush=True)
        # return outp

async def shell_output():
    global total
    while True:
        await asyncio.sleep(0.5)
        try:
            pass
            # total = int(weight1.split()[1]) + int(weight2.split()[1]) + int(weight3.split()[1])
            # print(weight1)
            # print(weight2)
            # print(weight3)
            # print(total)
        except NameError:
            continue

loop = asyncio.get_event_loop()

async def main():
    loop.create_task(output(h1))
    loop.create_task(output(h2))
    loop.create_task(output(h3))
    loop.create_task(shell_output())
    loop.create_task(app())
    # loop.run_forever()

asyncio.run(main())

# reader, writer = loop.run_until_complete(s1)
# reader, writer = loop.run_until_complete(s2)
# reader, writer = loop.run_until_complete(s3)
# loop.run_until_complete(shell_output())
# loop.run_until_complete(app())

# loop.run_until_complete(writer.protocol.waiter_closed)