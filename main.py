import csv
import hashlib
import json
import socket
import threading
import time
import rsa
from rich import print
import db_connect as db
import client_obj as obj  # Ensure this is properly implemented
from client import rcv as r

buffer = 1024
connected_clients = {}  # Dictionary to manage connected clients

def get_db():
    return db.connect_db("localhost", "root", "toor", "licenta")

def hash_hwid(hwid):
    sha256 = hashlib.sha256()
    sha256.update(hwid.encode('utf-8'))
    return sha256.hexdigest()

def hardware_info(client_socket, private_key):
    print("Gathering hardware information")
    try:
        dump = 1
        list = []
        while dump != 0:
            data = r.rcv_msg(client_socket, private_key)
            if data == '0':
                dump = 0
            else:
                list.append(data)
        recreated_json_string = [''.join(item.split('\n')) for item in list]
        recreated_json_string = '\n'.join(recreated_json_string)
        print(recreated_json_string)
        try:
            json_data = json.loads(recreated_json_string)
            with open('received_data.csv', 'a', newline='') as csvfile:
                fieldnames = json_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(json_data)
                print("JSON data saved to received_data.csv")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def client_input_thread(client_socket, client_id, public_key, private_key):
    try:
        while True:
            option = input(f"Client {client_id}: Enter your option (1-Hardware) (2-Updates) (3-Printers) (4-List Clients) (5-Send Command) (S-Switch Client): ")
            if option == '1':
                r.send_msg(option, client_socket, public_key)
                hardware_info(client_socket, private_key)
            elif option == '2':
                r.send_msg(option, client_socket, public_key)
                while True:
                    response = r.rcv_msg(client_socket, private_key)
                    if response == '0':
                        break
                    print(response)
            elif option == '3':
                r.send_msg(option, client_socket, public_key)
                while True:
                    response = r.rcv_msg(client_socket, private_key)
                    if response == '0':
                        break
                    print(response)
            elif option == '4':
                list_connected_clients()
            elif option == '5':
                command = input("Enter the command to send to all clients: ")
                send_command_to_all_clients(command.encode('UTF-8'))
            elif option.lower() == 's':
                switch_client(private_key)
            elif option == '0':
                break
            else:
                print("Invalid option. Choose 1, 2, 3, 4, 5, S, or 0 to exit.")
    except ConnectionResetError:
        print(f"Client {client_id} has lost connection.")
        del connected_clients[client_id]
        client_socket.close()
    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
def list_connected_clients():
    dbs=get_db()
    connected_clients = db.selectare_inregistrari(dbs,"users","number_client")
    print("Connected Clients:")
    for ids in connected_clients:
        for client_id in ids:
            print(f"Client ID: {client_id}")

def send_command_to_all_clients(command):
    for client_id, client in connected_clients.items():
        try:
            client.socket.send(command)
            print(f"Sent command to Client {client_id}")
        except Exception as e:
            print(f"Failed to send command to Client {client_id}: {e}")

def switch_client(private_key):
    print("Available Clients:")
    for client_id, client in connected_clients.items():
        print(f"{client_id} - {client['address']}")
    select_client = int(input("Select client ID:"))
    if select_client in connected_clients:
        client = connected_clients[select_client]
        client_input_thread(client['socket'], client['client_id'], client['public_key'], private_key)

def accept_client_connections(server_socket, private_key, public_key):
    no = 1
    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.send(public_key.save_pkcs1("PEM"))
        public_key_data = rsa.PublicKey.load_pkcs1(client_socket.recv(buffer))
        hwid = r.rcv_msg(client_socket, private_key)
        client_id = hash_hwid(hwid)
        dbs = get_db()
        if db.selectare_inregistrare(dbs,"users","id_client","'{id_client}'= '{client_id}'") is None:
            db.adaugare_inregistrare(dbs, "users",{"id_client":client_id,"public_client":str(public_key_data) ,"ip_client":client_address[0],"number_client":no})
        else:
            connected_clients[client_id] = client_socket  # Store client socket for command sending
            threading.Thread(target=client_input_thread, args=(client_socket, client_id, public_key_data, private_key)).start()
            no += 1

def main():
    public_key, private_key = rsa.newkeys(1024)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 44452))
    server_socket.listen(5)
    print("Server is listening for incoming connections...")
    try:
        accept_client_connections(server_socket, private_key, public_key)
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
