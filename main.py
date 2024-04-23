import csv
import json
import socket
import threading
import time
import rsa
from client_obj import Client
from rich import *
from client import rcv as r
buffer = 1024


def hardware_info(client_socket, private_key):
    print("Gathering hardware information")
    try:
        dump = 1
        list=[]
        # Receive data from the client
        while dump != 0:
            data = r.rcv_msg(client_socket, private_key)
            if data == '0':
                dump =0
            else:
                list.append(data)
        recreated_json_string = [''.join(item.split('\n')) for item in list]
        recreated_json_string = '\n'.join(recreated_json_string)
        # Parse the received JSON data
        print(recreated_json_string)
        try:
            json_data = json.loads(recreated_json_string)

            # Save JSON data to a CSV file
            with open('received_data.csv', 'a', newline='') as csvfile:
                fieldnames = json_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the CSV file is empty and write the header if needed
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(json_data)
                print("JSON data saved to received_data.csv")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON data: {e}" )

    except Exception as e:
        print(f"An error occurred: {e}")


def list_connected_clients():
    print("Connected Clients:")
    for client_id, _ in connected_clients.items():
        print(f"Client ID: {client_id}")


def send_command_to_all_clients(command,public_key):
    for client_id, client_socket in connected_clients.items():
        try:
            r.send_msg()
            print(f"Sent '{command}' to Client {client_id}")
        except Exception as e:
            print(f"Failed to send command to Client {client_id}: {e}")


def switch_client(private_key):
    selectClient = int(input("Select client:"))
    returner = connected_clients[selectClient]
    client_input(returner.sockett, returner.client_id, returner.publickey, private_key)

def meniu(private_key):
    option = input("Enter your option (1-Select client) (2-Send command to all clients) (3-List of clients): ")
    if option == '1':
        print(f"Sunt {len(connected_clients)+1} conectati")
        switch_client(private_key)
    if option =='2':
        send_command_to_all_clients
def client_input(client_socket, client_id, public_key, private_key):

    try:
        while True:
            option = input("Ai urmatoarele optiuni: (1-Hardware) (2-Updates) (3-Printers)")
            if option == '0':
                r.send_msg(option, client_socket, public_key)
                break
            elif option == '1':
                r.send_msg(option, client_socket, public_key)
                hardware_info(client_socket, private_key)
            elif option == '2':
                r.send_msg(option, client_socket, public_key)
                while True:
                    response = r.rcv_msg(client_socket, private_key)
                    if response != '0' and response != "rasp":
                        print(response)
                    elif response == "rasp":
                        data = input()
                        r.send_msg(data, client_socket, public_key)
                    else:
                        break
            elif option == '3':
                r.send_msg(option, client_socket, public_key)
                while True:
                    response = r.rcv_msg(client_socket, private_key)
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
                print("Opiune invalida.Alege din 1, 2, 3, 4, 5, S, 9 sau 0 pentru a iesi.")
    except ConnectionResetError:
        print(f"Client {client_id} has lost connection.")
        del connected_clients[client_id]  # Remove the client socket from the dictionary
        client_socket.close()  # Close the client socket
    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")

def check_connections():
    while True:
        clients_to_check = dict(connected_clients.copy())
        for client_socket,_ in clients_to_check.items():
            try:
                r.send_msg((b'ping',_.client_id,_.publickey))
            except:
                print(f"[CLIENT {_.sockett.getpeername()[1]} DISCONNECTED]")
                connected_clients.pop(client_socket)
            time.sleep(10)  # Verificați conexiunile la fiecare 5 secunde
def conexiune():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.send(public_key.save_pkcs1("PEM"))
        rsa.PublicKey.load_pkcs1(client_socket.recv(buffer))
    server_socket.close()
public_key, private_key = rsa.newkeys(1024)
server_address = ('localhost', 44452)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Se asteapta conexiuni")
client_counter = 1
connected_clients={}
connection_thread = threading.Thread(target=conexiune)
connection_thread.start()
checker_thread = threading.Thread(target=check_connections)
checker_thread.daemon = True
checker_thread.start()
meniu(private_key)

# Close the server socket when exiting

