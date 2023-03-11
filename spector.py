import tkinter as tk
import socket
from plyer import notification
import threading
import datetime

class ChatClient:
    def __init__(self):
        # Set up the GUI
        self.root = tk.Tk()
        self.root.title("inverse")

        self.host_label = tk.Label(self.root, text="IP address:")
        self.host_label.pack()
        self.host_entry = tk.Entry(self.root)
        self.host_entry.pack()

        self.port_label = tk.Label(self.root, text="Port number:")
        self.port_label.pack()
        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack()

        self.text_box = tk.Text(self.root, height=50, width=50)
        self.text_box.pack(side=tk.LEFT)
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)

        self.input_box = tk.Entry(self.root, width=75)
        self.input_box.pack(side=tk.LEFT)
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Initialize instance variables
        self.socket = None
        self.connected = False

        # Start the GUI
        self.root.mainloop()

    def connect_to_server(self):
        # Get the host and port from the GUI
        host = self.host_entry.get()
        port = int(self.port_entry.get())

        # Connect to the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.connected = True

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while self.connected:
            try:
                message = self.socket.recv(1024).decode()
                self.text_box.insert(tk.END, message + "\n")
                # Notos
                notification.notify(
                title="inverse client",
                message=f"{message}",
                app_name="inverse",
                timeout=5
                )
                print(message)
                #save text
                now = datetime.datetime.now()
                file = open('messages.txt', 'a')
                file.write(str(now.day) + "/" + str(now.hour) + ":" + str(now.minute) + " " + message + "\n")
                file.close()
            except OSError:
                break

    def send_message(self):
        if self.connected:
            message = self.input_box.get()
            self.socket.send(message.encode())
            self.input_box.delete(0, tk.END)

if __name__ == '__main__':
    client = ChatClient()

