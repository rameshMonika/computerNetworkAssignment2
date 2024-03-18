import socket
import threading

# Function to handle client connections
def handle_client(client_socket, clients, client_names):
   
    try:
        
        client_socket.sendall(" ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        while username in client_names.values():
            client_socket.sendall("[Username has already been used. Please enter another name.]: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()

        client_names[client_socket] = username


        # Notify all other clients about the new client joining
        joined_message = f"[{username} joined]"
       
        for client in clients:
            if client != client_socket:
            
                client.sendall(joined_message.encode('utf-8'))

        # Send welcome message to client
        welcome_message = f"[Welcome {username}!]"
        client_socket.sendall(welcome_message.encode('utf-8'))
    

        while True:
            try:
                # Receive message from client
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    if message.strip() == "@quit":
                        break
                    elif message.strip() == "@names":
                        connected_users = ", ".join(client_names.values())
                        client_socket.sendall(f"[Connected users: {connected_users}]".encode('utf-8'))
                    elif message.startswith("@"):
                        recipient, msg_content = message.split(" ", 1)
                        recipient = recipient[1:]  
                        for client_sock, name in client_names.items():
                            if name == recipient:
                                client_sock.sendall(f"[{username} (private)]: {msg_content}".encode('utf-8'))
                                break
                    else:
                        formatted_message = f"[{username}:] {message}"
                        # Broadcast message to all clients
                        for client in clients:
                            if client != client_socket:
                                client.sendall(formatted_message.encode('utf-8'))

            except Exception as e:
                print(f"Error receiving message from client: {e}")
                break

        # Notify other clients about the client's departure
        left_message = f"[{client_names[client_socket]} left]"

        # Remove client from list and close connection
        for client in clients:
            if client != client_socket:
                client.sendall(left_message.encode('utf-8'))

        clients.remove(client_socket)
        client_socket.close()

        del client_names[client_socket]
    except Exception as e:
        print(f"Error handling client: {e}")


# Main function
def main():
    # Server configuration
    host = 'localhost'
    port = 8888

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    clients = []
    client_names = {}

    while True:
        # Accept client connection
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

     

        # Add client to list
        clients.append(client_socket)

        # Create thread to handle client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, client_names))
        client_thread.start()

    server_socket.close()

if __name__ == "__main__":
    main()
