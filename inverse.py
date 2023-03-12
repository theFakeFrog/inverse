import socket
import threading
import json

# Load configuration from file
with open("config.json") as f:
    config = json.load(f)

federated_servers = config["federated_servers"]

# Stores clients and server info
clients = {}

# Handling incoming connections
def handle_client(conn, addr, server_id):
    with conn:
        print(f'Connected from server ID {server_id}')
        conn.sendall(b'Connected to server! This server is on version 0.3')  # welcome msg
        username = conn.recv(1024).decode()
        if len(username) > 20:
            conn.sendall(b'Username too long. Maximum 20 characters allowed.')
            conn.close()
            return
        # Add client to the dictionary with their username and server
        clients[conn] = (username, server_id)
        print(f'{username} has joined')
        # Broadcast a message to clients to notify of the new user
        for client, (client_username, client_server_id) in clients.items():
            client.sendall(f'{username} has joined the chat from server {server_id}'.encode())
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    raise Exception('Client disconnected')
                # Check if message length is valid
                if len(data) > 200:
                    conn.sendall(b'Message too long. Maximum 200 characters allowed.')
                    continue
                # Broadcast the message to all clients
                for client, (client_username, client_server_id) in clients.items():
                    client.sendall(f'{username}${server_id}: {data.decode()}'.encode())
        except Exception as e:
            print(e)
        # Remove the client and notify other clients
        del clients[conn]
        print(f'{username} has left the chat')
        for client, (client_username, client_server_id) in clients.items():
            client.sendall(f'{username} has left the chat from server {server_id}'.encode())

def handle_federated_server(server_id, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Listening on {host}:{port}...')
        while True:
            conn, addr = s.accept()
            # Make a new thread for each connection
            threading.Thread(target=handle_client, args=(conn, addr, server_id)).start()

# Create and start the threads for each server
for server_id, (host, port) in enumerate(federated_servers):
    threading.Thread(target=handle_federated_server, args=(server_id, host, port)).start()
