import socket
import threading
import os
IP = input("input ip: ")
print("default port 226")
HOST = IP     #server IP address
PORT = 226    #server port

def receive_messages():
    while True:
        #get messages from server
        message = s.recv(4096).decode()
        if not message:
            break
        print(message)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #welcome message and prompt for a username
    print(s.recv(1024).decode())
    username = input('username: ')
    s.sendall(username.encode())
    #Start a new thread to receive messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    while True:
        #Send messages to da server
        message = input('{username}:')
        s.sendall(message.encode())

