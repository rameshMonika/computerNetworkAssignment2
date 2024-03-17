import socket
import threading

# Function to receive messages from server
def receive_messages(client_socket):
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("["):
                print(message)
            else:
                print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

# Main function
def main():
    # Prompt user for server IP address, port number, and username
    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port number: "))
    username = input("Enter your username: ")

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return

    # Receive username prompt from server
    server_message = client_socket.recv(1024).decode('utf-8')
    print(server_message)

    # Send username to server
    client_socket.sendall(username.encode('utf-8'))

    # Receive welcome message from server
    welcome_message = client_socket.recv(1024).decode('utf-8')
    print(welcome_message)

   

    # Start thread to receive messages from server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()


    # Send messages to server
    while True:
        message = input()
        client_socket.sendall(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()

