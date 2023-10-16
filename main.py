import socket
import json
import csv
import signal
import threading
import sys

# Define the server IP and port
server_address = ('172.29.2.11', 4445)

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

def send_command_to_all_clients(command):
    for client_id, client_socket in connected_clients.items():
        try:
            client_socket.send(command.encode())
            print(f"Sent '{command}' to Client {client_id}")
        except Exception as e:
            print(f"Failed to send command to Client {client_id}: {e}")

def client_input_thread(client_socket, client_id):
    try:
        while True:
            option = input(f"Select an option for client {client_id} (1 - Hardware info, 2 - Update Windows, 3 - Printer List, 4 - List Clients, 5 - Send Command to All, 0 - Exit, S - Switch to another client): ")
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
            elif option == '4':
                list_connected_clients()
            elif option == '5':
                command = input("Enter the command to send to all clients: ")
                send_command_to_all_clients(command)
            elif option.lower() == 's':
                switch_client(client_socket)
            else:
                print("Invalid option. Choose 1, 2, 3, 4, 5, S, or 0 to exit.")
    except ConnectionResetError:
        print(f"Client {client_id} has lost connection.")
        del connected_clients[client_id]  # Remove the client socket from the dictionary
        client_socket.close()  # Close the client socket
    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
    finally:
        print(f"Client {client_id} has disconnected.")

def handle_client(client_socket, client_id):
    try:
        connected_clients[client_id] = client_socket
        print(f"Client {client_id} connected.")

        # Start a separate thread to handle user input
        input_thread = threading.Thread(target=client_input_thread, args=(client_socket, client_id))
        input_thread.daemon = True  # Set as a daemon thread to exit when the main program exits
        input_thread.start()

        print(f"\nServer is still active for client {client_id}\n")

    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
    finally:
        client_socket.close()
        del connected_clients[client_id]
        print(f"Client {client_id} has disconnected.")

def switch_client(client_socket):
    client_id_input = input("Enter the client ID to switch to (or 'list' to see connected clients): ")
    if client_id_input.lower() == 'list':
        list_connected_clients()
    else:
        try:
            client_id = int(client_id_input)
            if client_id in connected_clients:
                target_socket = connected_clients[client_id]
                while True:
                    command = input("Enter a command to send to the target client (or 'exit' to return to the menu): ")
                    if command.lower() == 'exit':
                        break
                    target_socket.send(command.encode())
                print(f"Switched to client {client_id}")
            else:
                print(f"Invalid client ID: {client_id}")
        except ValueError:
            print("Invalid input. Please enter a valid client ID or 'list'.")

def sigint_handler(sig, frame):
    print("\nCtrl+C received. Stopping the server...")
    global server_socket
    for client_id, client_socket in connected_clients.items():
        client_socket.close()
    server_socket.close()
    sys.exit(0)

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


signal.signal(signal.SIGINT, sigint_handler)

# Counter to assign unique client IDs
client_counter = 1

while True:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_id = client_counter
        client_counter += 1

        # Start a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")

# Close the server socket when exiting
server_socket.close()
