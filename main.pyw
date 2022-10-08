import tkinter as tk
import asyncio, socket

global ws
ws = {}

async def connection(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = s.recv(8096)
            print(f"{host} {data!r}")
            await asyncio.sleep(0.2)
            ws[host] = data.decode()

def draw(root):
    root.resizable(0, 0)
    # root.overrideredirect(1)
    root.attributes("-topmost", True)
    root.title("Weighbridge Scale")
    root.geometry("200x60")
    frame = tk.Frame(root, width=200, height=100, relief="solid")
    frame.place(x=10, y=10)
    text = tk.Label(
        frame,
        text="loading",
        font=("Helvetica", 20),
    )
    text.pack()
    return text

async def refresher():
    root = tk.Tk()
    text = draw(root)
    while True:
        total = float(0)
        for w in ws:
            w = ws[w][4:16]
            total += float(w.split()[0])
        text.configure(text=total / 1000)
        print(int(total))
        root.update()
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(
        refresher(),
        connection("192.168.10.200", 1749),
        connection("192.168.10.201", 1749),
        connection("192.168.10.202", 1749),
    )

asyncio.run(main())
