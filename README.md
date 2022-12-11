# Mettler Toledo Multistage IP Scale
A simple multistage weighing station program for Metterler Toledo Scales. 

Using Asyncio, TCP and Tkinter.

Run once to generate config file. The IP field can support 1 and more scales.

# How does it work?

The program is intended to connect to a Mettler Toledo IP Scale, it receives data over the network, and then display that data in a graphical user interface (GUI) created with the tkinter library.

The connection function creates a new socket connection to the specified host and port using the socket library. It then enters a loop where it waits for data to be received from the server, updates a global dictionary called ws with the received data, and then waits for a short amount of time before repeating the process.

The draw function creates the GUI by creating a new window using tkinter and adding a Frame and a Label to the window. The refresher function updates the text in the Label with the average value of all the entries in the ws dictionary.

The main function uses asyncio to run the refresher and connection functions concurrently. It creates a list of connection tasks, one for each IP address in the config.ips list, and then waits for all the tasks to complete using asyncio.gather.
