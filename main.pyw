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
                if close():
                    return
                data = await reader.read(8096)
                # print(f"{host} {data!r}")
                await asyncio.sleep(0.2)
                ws[host] = data.decode()
        except (socket.timeout, ConnectionError, OSError):
            if close():
                return
            ws[host] = -1
            print(f"Failed to connect to {host}:{port}. Retrying in 5 seconds.")
            await asyncio.sleep(5)

def close():
    try:
        if the_queue.queue[0] is None:
            print("connection thread: got None, exiting...")
            return True
    except:
        pass 

def updater():
    # print("Start weight update")
    neterror = False
    total = float(0)
    for w in ws:
        if ws[w] == -1:
            neterror = True
        else:
            w = ws[w][4:16]
            try:
                total += float(w.split()[0])
            except IndexError:
                neterror = True
                print("list index out of range")
    if neterror:
        reading.configure(text="Network Error")      
    else:
        scales.configure(text=f"⚖️ {len(ws)}")
        reading.configure(text=total / 1000)
    print(f"t: {int(total) :<8} s: {len(ws) :>1}")
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

def threadtarget():
    asyncio.run(corountine())

if __name__ == '__main__':
    # Intialise weight dict; Host, Value pair.
    ws = {}
    
    # Create Tkinter App
    root = tk.Tk()
    root.resizable(0, 0)
    # root.overrideredirect(1)
    root.attributes("-toolwindow", 1,"-topmost", 1)
    root.title("🚛 Weigh bridge scale")
    root.geometry(config.windowsposition)
    
    frame = tk.Frame(root, width=500, height=100, relief="solid")
    frame.pack(fill='both', expand=True)
    
    reading = tk.Label(frame, text="loading", font=("Helvetica", 20))
    reading.pack(side="left", padx=10,pady=10)

    scales = tk.Label(frame, text="⚖️ 0", font=("Helvetica", 15))
    scales.pack(side="right", padx=10)

    # Start Connection Thread
    threading.Thread(target=threadtarget).start()

    # Main loop for Tkinter App
    root.after(100, updater)
    root.mainloop()

    # Stop queue
    the_queue = queue.Queue()
    the_queue.put(None)