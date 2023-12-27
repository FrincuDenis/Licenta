import queue
import socket
import json
import csv
import signal
import threading
import sys
import client
# Define the server IP and port
server_address = ('localhost', 44452)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for incoming connections...")

# Lock for thread synchronization
connected_clients_lock = threading.Lock()
client_states = {}
# Dictionary to store connected clients and their sockets
connected_clients = {}
client_threads = {}
input_queue = queue.Queue()
def sigint_handler(sig, frame):
    print("\nCtrl+C received. Stopping the server...")
    global server_socket
    for client_id, client_socket in connected_clients.items():
        client_socket.close()
    server_socket.close()
    sys.exit(0)

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


def switch_client():
    print("Active Clients:")

    # Acquire the lock to ensure exclusive access to the connected_clients dictionary
    with connected_clients_lock:
        for client_id, thread in connected_clients.items():
            print(f"Client {client_id}")

    selected_client_id = int(input("Enter the client ID to switch to: "))
    if selected_client_id in connected_clients:
        client_thread = client_threads[selected_client_id]
        input_queue.put(f"S{selected_client_id}")
        client_thread.join()  # Wait for the client thread to complete the switch
    else:
        print(f"Invalid client ID: {selected_client_id}")

# Counter to assign unique client IDs
client_counter = 1
def client_input_thread(client_socket, client_id):
    try:
        while True:
            option = input_queue.get()
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
                switch_client()
            else:
                print("Invalid option. Choose 1, 2, 3, 4, 5, S, or 0 to exit.")
    except ConnectionResetError:
            print(f"Client {client_id} has lost connection.")
            del connected_clients[client_id]  # Remove the client socket from the dictionary
            del connected_clients[client_id]  # Remove the client thread from the dictionary
            client_socket.close()  # Close the client socket
    except Exception as e:
            print(f"An error occurred with client {client_id}: {e}")
    finally:
        print(f"Client {client_id} has disconnected.")

def process_input():
    while True:
        try:
            # Acquire the lock to ensure exclusive access to the connected_clients dictionary
            with connected_clients_lock:
                active_clients = [client_id for client_id, state in client_states.items() if state == 'active']
                print("Active Clients:")
                for client_id in active_clients:
                    print(f"Client {client_id}")

            selected_client_id = int(input("Enter the client ID to switch to: \n"))

            # Check if selected_client_id is in the dictionary before accessing its value
            if selected_client_id in client_states and client_states[selected_client_id] == 'active':
                client_thread = client_threads[selected_client_id]
                input_queue.put(f"S{selected_client_id}")
                client_thread.join()  # Wait for the client thread to complete the switch
            else:
                print(f"Invalid or inactive client ID: {selected_client_id}")

        except RuntimeError as e:
            print(f"Error during iteration: {e}")


input_thread_started = False

while True:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_id = client_counter
        client_counter += 1

        # Start a thread to handle the client
        try:
            thread = threading.Thread(target=client_input_thread, args=(client_socket, client_id))
            thread.daemon = True
            thread.start()
            connected_clients[client_id] = thread
            print(f"Client {client_id} connected.")
            print(f"Active Clients: {threading.active_count() - 2}")
            if not input_thread_started:
                input_thread = threading.Thread(target=process_input)
                input_thread.daemon = True
                input_thread.start()
                input_thread_started = True

        except Exception as e:
            print(f"An error occurred with client {client_id}: {e}")


    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"An error occurred: {e}")

# Close the server socket when exiting
server_socket.close()

'''
        finally:
            client_socket.close()
            del connected_clients[client_id]
            print(f"Client {client_id} has disconnected.")'''