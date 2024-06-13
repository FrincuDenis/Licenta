'''
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.client_address = None

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Connected to client at {self.client_address}")

    def return_client_socket(self):
        return self.client_socket

    def options(self, command):
        if command:
            if command == "1":
                self.client_socket.sendall(b"cpu_ram")
            elif command == "2":
                self.client_socket.sendall(b"power")
            elif command == "3":
                self.client_socket.sendall(b"battery")
            elif command == "4":
                self.client_socket.sendall(b"system_info")
            elif command == "5":
                self.client_socket.sendall(b"processes")
            elif command == "6":
                self.client_socket.sendall(b"sensor_data")
            elif command == "7":
                self.client_socket.sendall(b"storage_info")
            elif command == "8":
                self.client_socket.sendall(b"network_data")
            elif command == "9":
                self.client_socket.sendall(b"io")
            elif command == "10":
                self.client_socket.sendall(b"if_addr")
            elif command == "11":
                self.client_socket.sendall(b"connects")
            elif command == "12":
                self.client_socket.sendall(b"shutdown")
            print(f"Command sent to client.{command}")

    def receive_chunks(self, client_socket):
        # Receive data from client in chunks
        chunks = []
        while True:
            chunk = client_socket.recv(7168)
            if chunk != b'\0':
                chunks.append(chunk)
                time.sleep(0.1)
            else:
                break
        return b"".join(chunks)

    def process_response(self, response):
        # Process the received response here
        print("Received response from client:")
        print(response)

    def get_client_address(self):
        return self.client_address
'''
'''

import socket
import threading
import json
import time

from debugpy.adapter import clients

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}
        self.command_queue = []  # Queue to store commands and associated data
        self.chunk_size=4096
    def size(self):
        while True:
            if len(self.command_queue) == 11:
                return 1
    def handle_client(self, client_socket, client_address):
        client_name = client_socket.recv(1024).decode()
        self.clients[client_name] = client_socket
        print(f"New connection from {client_address} ({client_name})")

        try:
            while True:
                commands = ["cpu_ram", "power", "battery", "system_info", "processes", "network_data",
                            "storage_info", "sensor_data", "io", "if_addr", "connects","is_in_domain","fetch_all_user_info"]

                for command in commands:
                    time.sleep(0.5)
                    command = command.encode()+b"\1"
                    client_socket.send(command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received))
                     #   print(f"Response from {client_name} for {command_received}: {data_received}")
        except Exception as e:
            print(f"Connection to {client_name} lost: {e}")
        finally:
            client_socket.close()
            del self.clients[client_name]

    def receive_response(self, client_socket):
        response = []
        while True:
            chunk = client_socket.recv(self.chunk_size)
            if chunk[-1:] == b'\0':
                response.append(chunk[:-1])
                break
            response.append(chunk)

        response_data = b''.join(response).decode()
        try:
            json_response = json.loads(response_data)
            if isinstance(json_response, dict):
                for command, data in json_response.items():
                    return command, data
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        return None, None

    def get_next_command(self):
        # Get the next command and associated data from the queue
        if self.command_queue:
            return self.command_queue.pop(0)  # Pop the first element from the queue
        else:
            return None

    def data_send(self, data, name,command):
        client_socket=self.clients[name]
        data_to_send = json.dumps({command: data})
        for i in range(0, len(data_to_send), self.chunk_size):
            chunk = data_to_send[i:i + self.chunk_size]
            client_socket.sendall(chunk.encode())
            client_socket.sendall(b'\0')
            print(f"Command sent to client: {command}")
        client_socket.sendall(data)
        time.sleep(0.5)
    def stop(self):
        self.server_socket.close()
    def start(self):
        print(f"Server started at {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()

'''
import socket
import threading
import json
import time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = {}
        self.command_queue = []
        self.chunk_size = 4096

    def handle_client(self, client_socket, client_address):
        try:
            client_name = client_socket.recv(1024).decode()
            self.clients[client_name] = client_socket
            print(f"New connection from {client_address} ({client_name})")
            self.send_commands(client_socket, client_name)
        except Exception as e:
            print(f"Connection to {client_address} lost: {e}")
        finally:
            self.cleanup_client(client_socket, client_name)

    def send_commands(self, client_socket, client_name):
        commands = ["cpu_ram", "power", "battery", "system_info", "processes", "network_data",
                    "storage_info", "sensor_data", "io", "if_addr", "connects", "is_in_domain", "fetch_all_user_info"]
        while True:
            for command in commands:
                try:
                    time.sleep(1)
                    self.send_command(client_socket, command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received))
                except Exception as e:
                    print(f"Error handling command {command} for {client_name}: {e}")

    def send_command(self, client_socket, command):
        full_command = command.encode() + b"\1"
        client_socket.sendall(full_command)
        print(f"Sent command to client: {command}")

    def receive_response(self, client_socket):
        response = []
        while True:
            chunk = client_socket.recv(self.chunk_size)
            if not chunk:
                raise ConnectionError("Connection closed by client")
            if chunk[-1:] == b'\0':
                response.append(chunk[:-1])
                break
            response.append(chunk)

        response_data = b''.join(response).decode()
        try:
            json_response = json.loads(response_data)
            if isinstance(json_response, dict):
                for command, data in json_response.items():
                    return command, data
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        return None, None

    def get_next_command(self):
        if self.command_queue:
            return self.command_queue.pop(0)
        return None

    def data_send(self, data, name, command):
        client_socket = self.clients.get(name)
        if not client_socket:
            print(f"No client found with name {name}")
            return

        data_to_send = json.dumps({command: data})
        for i in range(0, len(data_to_send), self.chunk_size):
            chunk = data_to_send[i:i + self.chunk_size]
            client_socket.sendall(chunk.encode())
        client_socket.sendall(b'\0')
        print(f"Command sent to client: {command}")

    def cleanup_client(self, client_socket, client_name):
        client_socket.close()
        if client_name in self.clients:
            del self.clients[client_name]
        print(f"Cleaned up client {client_name}")

    def stop(self):
        self.server_socket.close()
        print("Server stopped")

    def start(self):
        print(f"Server started at {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            self.stop()

if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
