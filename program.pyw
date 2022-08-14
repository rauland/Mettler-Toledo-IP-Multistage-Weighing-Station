import tkinter as tk
import asyncio
import telnetlib3
global w1
global w2
global w3

async def shell1(reader, writer):
    i = '1'
    global w1
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        w1 = f'{i}{outp}'

async def shell2(reader, writer):
    i = '2'
    global w2
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        w2 = f'{i}{outp}'

async def shell3(reader, writer):
    i = '3'
    global w3
    while True:
        # read stream until '?' mark is found
        outp = await reader.read(1024)
        # display all server output
        # print(i+outp, flush=True)
        w3 = f'{i}{outp}'

loop = asyncio.get_event_loop()

s1 = telnetlib3.open_connection('192.168.10.200', 1749, shell=shell1)
s2 = telnetlib3.open_connection('192.168.10.201', 1749, shell=shell2)
s3 = telnetlib3.open_connection('192.168.10.202', 1749, shell=shell3)

reader, writer = loop.run_until_complete(s1)
reader, writer = loop.run_until_complete(s2)
reader, writer = loop.run_until_complete(s3)
# loop.run_until_complete(shell_output())
    
def Draw():
    global text
    root.resizable(0,0)
    # root.overrideredirect(1)
    root.attributes('-topmost', True)
    root.title("Weighbridge Scale")
    root.geometry("200x100")
    frame=tk.Frame(root,width=200,height=100,relief='solid')
    frame.place(x=10,y=10)
    text=tk.Label(
        frame,
        text='loading',
        font=("Helvetica", 20),
        )
    text.pack()

async def Refresher():
    global text
    while True:
        try:
            total = float(w1.split()[1]) + float(w2.split()[1]) + float(w3.split()[1])
            # total = 6000 + 4000 + 5000
            text.configure(text=total/1000)
            print(int(w1.split()[1]) + int(w2.split()[1]) + int(w3.split()[1]))
        except NameError:
            print("loading")
        root.update()
        await asyncio.sleep(0.1)
        root.after(1000, Refresher) # every second...

root=tk.Tk()
Draw()
loop.run_until_complete(Refresher())
root.mainloop()

# loop.run_until_complete(writer.protocol.waiter_closed)