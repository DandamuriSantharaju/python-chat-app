
import socket
import threading

clients = []

def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            broadcast(msg.decode(), client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Don't send the message back to the sender
            try:
                client.send(message.encode())
            except:
                clients.remove(client)
                client.close()

def start_server(host="localhost", port=5555):
    server = socket.socket()
    server.bind((host, port))
    server.listen()
    print(f"Server is running on {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
        thread.start()

start_server()

