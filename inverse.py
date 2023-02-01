import socket
import threading

# List of all federated servers
#federated_servers = [('127.0.0.1', 226), ('127.0.0.1', 227), ('127.0.0.1', 228)]
federated_servers = [('192.168.1.4', 226)]
# Stores clients and their associated server
clients = {}

# Handling incoming connections
def handle_client(conn, addr, server_id):
    with conn:
        print(f'Connected by {addr}')
        conn.sendall(b'Connected to server!')  #welcome msg
        username = conn.recv(1024).decode()
        # Add client to the dictionary with their username and associated server
        clients[conn] = (username, server_id)
        print(f'{username} has joined')
        # Broadcast a message to all clients to notify of the new user
        for client, (client_username, client_server_id) in clients.items():
            client.sendall(f'{username} has joined the chat from server {server_id}'.encode())
        while True:
            data = conn.recv(4096)
            if not data:
                break
            # Broadcast the message to every client
            for client, (client_username, client_server_id) in clients.items():
                client.sendall(f'{username}@{server_id}: {data.decode()}'.encode())
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

# Create and start the threads for each federated server
for server_id, (host, port) in enumerate(federated_servers):
    threading.Thread(target=handle_federated_server, args=(server_id, host, port)).start()

