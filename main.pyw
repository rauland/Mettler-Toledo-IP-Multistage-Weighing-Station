"""Weigh Bridge Module"""
import tkinter as tk
import asyncio
import socket
import threading
import config

async def connection(host, port):
    while not STOP:
        try:
            reader, _ = await asyncio.open_connection(host, port)
            while not STOP:
                data = await reader.read(8096)
                # print(f"{host} {data!r}")
                await asyncio.sleep(0.2)
                weights[host] = data.decode()
        except (socket.timeout, ConnectionError, OSError):
            weights[host] = -1
            print(f"Failed to connect to {host}:{port}. Retrying in 5 seconds.")
            await asyncio.sleep(5)
    if STOP:
        print("connection thread: got STOP, exiting...")

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
    """Starts new thread for asyncio"""
    asyncio.run(corountine())

class App():
    """APP GUI Class"""
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        # root.overrideredirect(1)
        self.root.attributes("-toolwindow", 1,"-topmost", 1)
        self.root.title("🚛 Weigh bridge scale")
        self.root.geometry(config.windowsposition)

        self.frame = tk.Frame(self.root, width=500, height=100, relief="solid")
        self.frame.pack(fill='both', expand=True)

        self.reading = tk.Label(self.frame, text="loading", font=("Helvetica", 20))
        self.reading.pack(side="left", padx=10,pady=10)

        self.scales = tk.Label(self.frame, text="⚖️ 0", font=("Helvetica", 15))
        self.scales.pack(side="right", padx=10)

    def update(self):
        """Updates values in GUI"""
        # print("Start weight update")
        neterror = False
        total = float(0)
        for host, weight in weights.items():
            if weight == -1:
                neterror = True
            else:
                w = weight[4:16]
                try:
                    total += float(w.split()[0])
                except IndexError:
                    neterror = True
                    print(f"{host}'s list index out of range")
        if neterror:
            self.reading.configure(text="Network Error")
        else:
            self.scales.configure(text=f"⚖️ {len(weights)}")
            self.reading.configure(text=total / 1000)
        print(f"t: {int(total) :<8} s: {len(weights) :>1}")
        self.root.after(100, self.update)
        # print("End weight update")

if __name__ == '__main__':
    # Intialise weights dict; (Host: Value)
    weights = {}
    STOP = False
    # Create tinker app
    app = App()

    # Start Connection Thread for asyncio functions
    threading.Thread(target=threadtarget).start()

    # Main loop for Tkinter App
    app.root.after(100, app.update)
    app.root.mainloop()

    # Stop queue
    STOP = True
