import tkinter as tk
import asyncio
import socket
import config
import threading
import queue

async def connection(host, port):
    while True:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            while True:
                if checkclose():
                    return
                data = await reader.read(8096)
                # print(f"{host} {data!r}")
                await asyncio.sleep(0.2)
                ws[host] = data.decode()
        except (socket.timeout, ConnectionError, OSError):
            if checkclose():
                return
            ws[host] = -1
            print(f"Failed to connect to {host}:{port}. Retrying in 5 seconds.")
            await asyncio.sleep(5)

def checkclose():
    try:
        message = the_queue.get_nowait()
        if message is None:
            print("thread_target: got None, exiting...")
            return True
    except:
        pass 

def updater():
    # print("Start weight update")
    total = float(0)
    for w in ws:
        if ws[w] == -1:
            text.configure(text="Network Error")
            # print(w +" Re-establishing connection")
        else:
            w = ws[w][4:16]
            try:
                total += float(w.split()[0])
            except IndexError:
                text.configure(text="Index Error")
                print("list index out of range")
    text.configure(text=total / 1000)
    print(int(total))
    root.after(100, updater)
    # print("End weight update")

async def corountine():
    connection_list =[]
    for ip in config.ips:
        connection_list += [
            connection(ip,config.port),
        ]
    await asyncio.gather(
        *connection_list,
    )

def main():
    asyncio.run(corountine())

if __name__ == '__main__':
    ws = {}
    
    # Create Tkinter App
    root = tk.Tk()
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

    # Start Connection Thread
    threading.Thread(target=main).start()

    # Main loop for Tkinter App
    root.after(100, updater)
    root.mainloop()

    # Stop queue
    the_queue = queue.Queue()
    the_queue.put(None)