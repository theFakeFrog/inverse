import socket
import sys
from plyer import notification
import threading
import json

# Load config file
with open("userconfig.json") as f:
    config = json.load(f)

    federated_servers = config["federated_servers"]

print("Enter the federated server ID you want to connect to:")
for i, (host, port) in enumerate(federated_servers):
    print(f"{i}: {host}:{port}")

server_id = int(input().strip())
host, port = federated_servers[server_id]

notification.notify(
    title="inverse client",
    message=f"connected to server ID {i}",
#    app_icon='inverse.png',
    app_name="inverse",
    timeout=5
)

def receive_messages(s):
    while True:
        # get messages from server
        message = s.recv(4096).decode()
        if not message:
            break
        print(message)
        notification.notify(
    title="inverse client",
    message=f"{message}",
#    app_icon='inverse.png',
    app_name="inverse",
    timeout=5
)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    # welcome message and prompt for a username
    print(s.recv(1024).decode())
    username = input('username: ')
    s.sendall(username.encode())
    # start a new thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()
    while True:
        # Send messages to da server
        message = input(':')
        s.sendall(message.encode())

    s.close()
    print("Connection closed")
