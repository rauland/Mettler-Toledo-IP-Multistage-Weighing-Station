"""Weigh Bridge Module"""
import tkinter as tk
import socket
import threading
import time
import config

class Connection:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.weight = ""
        self.stop = False

    def connection(self):
        while not self.stop:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    while not self.stop:
                        data = s.recv(8096)
                        time.sleep(0.2)
                        self.weight = data.decode()
            except (socket.timeout, ConnectionError, OSError):
                self.weight = -1
                print(f"Failed to connect to {self.host}:{self.port}. Retrying in 5 seconds.")
                time.sleep(5)
        if self.stop:
            print(f"connection {self.host}: got STOP, exiting...")

class App:
    """APP GUI Class"""
    def __init__(self) -> None:
        self.weights = []
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
        for scale in self.weights:
            if scale.weight == -1:
                neterror = True
            else:
                weight = scale.weight[4:16]
                try:
                    total += float(weight.split()[0])
                except IndexError:
                    neterror = True
                    print(f"{scale.host}'s list index out of range")
        if neterror:
            self.reading.configure(text="Network Error")
        else:
            self.scales.configure(text=f"⚖️ {len(self.weights)}")
            self.reading.configure(text=total / 1000)
        print(f"t: {int(total) :<8} s: {len(self.weights) :>1}")
        self.root.after(100, self.update)
        # print("End weight update")

    def connections(self):
        for ip in config.ips:
            self.weights +=[
                Connection(ip,config.port),
            ]
        for weight in self.weights:
            threading.Thread(target=weight.connection).start()

if __name__ == '__main__':
    # Create tinker app
    app = App()
    # Start Connection Threads
    app.connections()
    # Main loop for Tkinter App
    app.root.after(100, app.update)
    app.root.mainloop()
    # Stop Connection threads
    for connection in app.weights:
        connection.stop = True
