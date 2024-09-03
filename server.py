import socketserver
import time
import random

# Mimic Scale Data
def scale(weight = 0, change = 0):
    number = weight + change
    number = 0 if number < 0 else number
    formatted_number = "{:04d}".format(number)
    return number, f"zero {formatted_number} one two three"

class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print("{} Connected.".format(self.client_address[0]))
        weight, text = scale()
        while True:
            self.request.sendall(text.encode())
            time.sleep(0.01)

            # This will increase scale weight slowly
            ran = random.randint(0, 1000)
            if ran > 900:
                weight, text = scale(weight, 20)
            if ran < 50:
                weight, text = scale(weight, -20)

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1749

    # Create the server, binding to localhost on port 1749
    server = socketserver.TCPServer((HOST, PORT), TCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
