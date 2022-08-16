import tkinter as tk
import asyncio, socket
global ws
ws = {}

async def connection(host, port, con_num):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # s.sendall(b"Hello, world")
        
        while True:
            data = s.recv(8096)
            print(f"{con_num} {data!r}")
            await asyncio.sleep(0.2)
            ws[con_num] = data.decode()
   
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
            w1 = ws[1][4:16];w2 = ws[2][4:16];w3 = ws[3][4:16]
            total = float(w1.split()[0]) + float(w2.split()[0]) + float(w3.split()[0])
            # total = 6000 + 4000 + 5000
            text.configure(text=total/1000)
            print(int(w1.split()[1]) + int(w2.split()[1]) + int(w3.split()[1]))
        except NameError:
            print("loading")
        except KeyError:
            print("loading")
        root.update()
        await asyncio.sleep(0.1)
        # root.after(1000, Refresher) # every second...
root=tk.Tk()
Draw()

async def main():
    await asyncio.gather(
        connection('192.168.10.200', 1749,1),
        connection('192.168.10.201', 1749,2),
        connection('192.168.10.202', 1749,3),
        Refresher()
        )
    # loop.run_until_complete(Refresher())
asyncio.run(main())
root.mainloop()

# loop.run_until_complete(writer.protocol.waiter_closed)