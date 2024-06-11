import csv
import hashlib
import json
import socket
import threading
import time
import rsa
from rich import print
import db_connect as db
import client_obj as obj
from client import rcv as r


class Server:
    def __init__(self):
        self.connected_clients = {}
        self.buffer = 1024
        self.public_key, self.private_key = rsa.newkeys(1024)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 44452))
        self.server_socket.listen(5)
        print("Server is listening for incoming connections...")

    def run(self):
        threading.Thread(target=self.heartbeat, daemon=True).start()
        try:
            self.accept_client_connections()
        finally:
            self.server_socket.close()

    def get_db(self):
        return db.conectare_bd("localhost", "root", "toor", "licenta")

    def hash_hwid(self, hwid):
        sha256 = hashlib.sha256()
        sha256.update(hwid.encode('utf-8'))
        return sha256.hexdigest()

    def hardware_info(self, client_socket):
        print("Gathering hardware information")
        try:
            dump = 1
            list = []
            while dump != 0:
                data = r.rcv_msg(client_socket, self.private_key)
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

    def client_input_thread(self, client_socket, client_id, public_key):
        try:
            while True:
                option = input(
                    f"Client {client_id}: Enter your option (1-Hardware) (2-Updates) (3-Printers) (4-List Clients) (5-Send Command) (S-Switch Client): ")
                if option == '1':
                    r.send_msg(option, client_socket, public_key)
                    self.hardware_info(client_socket)
                # Handle other options similarly
                elif option == '0':
                    break
        except ConnectionResetError:
            print(f"Client {client_id} has lost connection.")
            del self.connected_clients[client_id]
            client_socket.close()
        except Exception as e:
            print(f"An error occurred with client {client_id}: {e}")

    def list_connected_clients(self):
        print("Connected Clients:")
        for client_id, _ in self.connected_clients.items():
            print(f"Client ID: {client_id}")

    def send_command_to_all_clients(self, command):
        for client_id, client in self.connected_clients.items():
            try:
                client.sockett.send(command)
                print(f"Sent command to Client {client_id}")
            except Exception as e:
                print(f"Failed to send command to Client {client_id}: {e}")

    def heartbeat(self):
        while True:
            to_remove = []
            for client_id, client in list(self.connected_clients.items()):
                try:
                    client.sockett.settimeout(2)
                    r.send_msg('ping', client.sockett, client.publickey)
                    if r.rcv_msg(client.sockett, self.private_key) != 'pong':
                        raise socket.timeout("No pong received")
                    client.sockett.settimeout(None)  # Reset the timeout
                except (socket.timeout, socket.error) as e:
                    print(f"Heartbeat failed for client {client_id}, removing from active clients.")
                    to_remove.append(client_id)
            for client_id in to_remove:
                del self.connected_clients[client_id]
            time.sleep(10)  # Check every 10 seconds

    def accept_client_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            client_socket.send(self.public_key.save_pkcs1("PEM"))
            public_key_data = rsa.PublicKey.load_pkcs1(client_socket.recv(self.buffer))
            client_id = len(self.connected_clients) + 1
            self.connected_clients[client_id] = obj.Client(client_id, client_socket, public_key_data)
            threading.Thread(target=self.client_input_thread, args=(client_socket, client_id, public_key_data)).start()


if __name__ == '__main__':
    server = Server()
    server.run()
