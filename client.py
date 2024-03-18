# import socket module for socket operations
# import threading module for multi-threading support

import socket
import threading

# Function to receive messages from server
def receive_messages(client_socket):
    # Loop to continuously receive messages from the server
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode('utf-8')
            # Check if the message is a system message (starts with "[")
            if message.startswith("["):
                print(message)
            else:
                # Print the received message
                print(message)
        except Exception as e:
            # Print any errors that occur during message reception
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
        # Print an error message if connection to the server fails
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

    # Loop to send messages to the server
    while True:
        message = input()
        if message.startswith("@group set"):
            client_socket.sendall(message.encode('utf-8'))
        else:
            client_socket.sendall(message.encode('utf-8'))

    # Close the client socket when the loop breaks
    client_socket.close()

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()
