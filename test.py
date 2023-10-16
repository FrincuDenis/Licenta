import socket
import json
import csv
import signal
import threading
import sys

# Define the server IP and port
server_address = ('172.29.2.11', 4445)
#server_address = ('localhost', 8888)
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for incoming connections...")

# Lock for thread synchronization
lock = threading.Lock()

# Dictionary to store connected clients and their sockets
connected_clients = {}


def list_connected_clients():
    print("Connected Clients:")
    for client_id, _ in connected_clients.items():
        print(f"Client ID: {client_id}")


def client_input_thread(client_socket, client_id):
    try:
        while True:
            option = input(f"Select an option for client {client_id} (1 - Hardware info, 2 - Update Windows, 3 - Printer List, 0 - Exit, S - Switch to another client): ")
            if option == '0':
                client_socket.send(option.encode())  # Send the exit signal to the client
                break
            elif option == '1':
                client_socket.send(option.encode())
                hardware_info(client_socket)
            elif option == '2':
                client_socket.send(option.encode())
                while True:
                    response = client_socket.recv(1024).decode()
                    if response != '0' and response != "rasp":
                        print(response)
                    elif response == "rasp":
                        data = input()
                        client_socket.send(data.encode())
                    else:
                        break
            elif option == '3':
                client_socket.send(option.encode())
                while True:
                    response = client_socket.recv(1024).decode()
                    if response != '0':
                        print(response)
                    else:
                        break
            elif option.lower() == 's':
                switch_client(client_socket)
            else:
                print("Invalid option. Choose 1, 2, 3, S, or 0 to exit.")
    except ConnectionResetError:
        print(f"Client {client_id} has lost connection.")
        del connected_clients[client_id]  # Remove the client socket from the dictionary
        client_socket.close()  # Close the client socket
    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
    finally:
        print(f"Client {client_id} has disconnected.")


def add_client(client_socket):
    global client_counter
    with lock:
        client_id = client_counter
        client_counter += 1
        connected_clients[client_id] = client_socket
    return client_id

def handle_client(client_socket):
    try:
        client_id = add_client(client_socket)  # Add the client to the dictionary

        print(f"Client {client_id} connected.")

        print(f"\nServer is still active for client {client_id}\n")

        while True:
            # Add any other server-side logic here
            pass

    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
    finally:
        client_socket.close()
        print(f"Client {client_id} has disconnected.")



def switch_client(client_socket):
    client_id = int(input("Enter the client ID to switch to (or 'list' to see connected clients): "))

    # Check if the input is the "list" command
    if client_id.lower() == 'list':
        list_connected_clients()
        return

    # Check if the specified client ID is valid
    if client_id in connected_clients:
        target_socket = connected_clients[client_id]
        while True:
            command = input("Enter a command to send to the target client (or 'exit' to return to the menu): ")
            if command.lower() == 'exit':
                break
            target_socket.send(command.encode())
    else:
        print(f"Invalid client ID: {client_id}")


def sigint_handler(sig, frame):
    print("\nCtrl+C received. Stopping the server...")
    # Close all client sockets
    for client_id, client_socket in connected_clients.items():
        client_socket.close()
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)

# Counter to assign unique client IDs
client_counter = 1


def hardware_info(client_socket):
    print("Gathering hardware information")
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        print("Received data from client")

        # Parse the received JSON data
        try:
            json_data = json.loads(data)
            print("Received JSON data:")
            print(json.dumps(json_data, indent=2))

            # Save JSON data to a CSV file
            with open('received_data.csv', 'a', newline='') as csvfile:
                fieldnames = json_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the CSV file is empty and write the header if needed
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(json_data)
                print("JSON data saved to received_data.csv")
        except json.JSONDecodeError:
            print("Failed to parse JSON data")

    except Exception as e:
        print(f"An error occurred: {e}")
# Function to send a command to all clients
def send_command_to_all_clients(command):
    for client_id, client_socket in connected_clients.items():
        try:
            client_socket.send(command.encode())
        except Exception as e:
            print(f"Failed to send command to client {client_id}: {e}")

# Function to send a command to a specific client
def send_command_to_client(client_id, command):
    if client_id in connected_clients:
        target_socket = connected_clients[client_id]
        try:
            target_socket.send(command.encode())
        except Exception as e:
            print(f"Failed to send command to client {client_id}: {e}")
    else:
        print(f"Invalid client ID: {client_id}")

# Function to handle server commands
def handle_server_commands():
    while True:
        command = input("Server Command (Type 'help' for available commands): ")
        if command == 'help':
            print("Available commands:")
            print("  - list: List connected clients")
            print("  - exit: Stop the server and disconnect all clients")
            print("  - sendall: Send a command to all clients")
            print("  - switch: Switch to a specific client or multiple clients by ID(s)")
            print("  - select: Select to a specific client")
        elif command == 'list':
            list_connected_clients()

        elif command == 'exit':
            print("Stopping the server...")
            for client_id, client_socket in connected_clients.items():
                client_socket.close()
            server_socket.close()
            sys.exit(0)


        elif command.startswith('sendall'):

            # Extract the command to send from the 'sendall' input

            parts = command.split(' ', 1)

            if len(parts) == 2:

                send_command_to_all_clients(parts[1])

            else:

                print("Usage: sendall <command>")

        elif command.startswith('switch'):

            # Extract the client IDs from the 'switch' input

            parts = command.split(' ', 1)

            if len(parts) == 2:

                client_ids = parts[1].split()  # Split the input into a list of client IDs

                for client_id in client_ids:

                    if client_id.isdigit():

                        send_command_to_client(int(client_id), "switch")

                    else:

                        print(f"Invalid client ID: {client_id}")

            else:

                print("Usage: switch <client_id1> <client_id2> ...")

        elif command.startswith('select'):
            try:
                client_id = int(command.split(' ', 1)[1])
                if client_id in connected_clients:
                    client_socket = connected_clients[client_id]
                    client_input_thread(client_socket, client_id)
                else:
                    print(f"Invalid client ID: {client_id}")
            except (ValueError, IndexError):
                print("Invalid 'select' command. Usage: select <client_id>")

        else:
            print("Unknown command. Type 'help' to see available commands.")



# Create a thread for handling server commands
command_thread = threading.Thread(target=handle_server_commands)
command_thread.daemon = True
command_thread.start()

# Continue with the rest of your server code

# Start the server
try:
    while True:
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

except KeyboardInterrupt:
    print("Server terminated by the user.")
    # Clean up and close sockets here
    server_socket.close()


