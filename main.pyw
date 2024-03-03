import tkinter as tk
import asyncio
import socket
import config

async def connection(host, port):
    while True:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            while True:
                data = await reader.read(8096)
                print(f"{host} {data!r}")
                await asyncio.sleep(0.2)
                ws[host] = data.decode()
        except (socket.timeout, ConnectionError, OSError):
            ws[host] = -1
            print(f"Failed to connect to {host}:{port}. Retrying in 5 seconds.")
            await asyncio.sleep(5)

def draw(root):
    root.resizable(0, 0)
    # root.overrideredirect(1)
    root.attributes("-toolwindow", 1,"-topmost", 1)
    root.title("🚛 Weigh bridge scale")
    root.geometry(config.windowsposition)
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
            while ws[w] == -1:
                text.configure(text="Network Error")
                # print(w +" Re-establishing connection")
                root.update()
                await asyncio.sleep(0.1)
            else:
                w = ws[w][4:16]
                try:
                    total += float(w.split()[0])
                except IndexError:
                    print("list index out of range")
                    # text.configure(text="Network Error")
                    # root.update()
        text.configure(text=total / 1000)
        print(int(total))
        root.update()
        await asyncio.sleep(0.1)

async def main():
    connection_list =[]
    for ip in config.ips:
        connection_list += [
            connection(ip,config.port),
        ]
    await asyncio.gather(
        refresher(),
        *connection_list,
    )

if __name__ == '__main__':
    ws = {}
    asyncio.run(main())