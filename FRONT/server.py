from PySide2.QtCore import QObject, Signal
import socket
import threading
import json
import time

'''
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
            client_hwid = client_socket.recv(1024).decode()
            self.clients[client_name] = client_socket
            print(f"New connection from {client_address} ({client_name}, {client_hwid})")
            self.send_commands(client_socket, client_name,client_hwid)
            self.send_commands(client_socket, client_hwid)
        except Exception as e:
            print(f"Connection to {client_address} lost: {e}")
        finally:
            self.cleanup_client(client_socket, client_name)

    def send_commands(self, client_socket, client_name,client_hwid):
        commands = ["get_group","cpu_ram", "power", "battery", "system_info", "processes", "network_data",
                    "storage_info", "sensor_data", "io", "if_addr", "connects", "is_in_domain", "fetch_all_user_info"]
        while True:
            print(f"list of clients: {self.clients}")
            for command in commands:
                try:
                    time.sleep(1)
                    self.send_command(client_socket, command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received,client_hwid))
                except Exception as e:
                    print(f"Error handling command {command} for {client_name}: {e}")

    def send_command(self, client_socket, command):
        full_command = command.encode() + b"\1"
        client_socket.sendall(full_command)
        print(f"Sent command to client: {command}")

    def receive_response(self, client_socket):
        response = bytearray()
        while True:
            chunk = client_socket.recv(self.chunk_size)
            if not chunk:
                raise ConnectionError("Connection closed by client")

            response.extend(chunk)

            # Check if the terminator is in the received chunk
            if b'\0' in chunk:
                break

        # Split the response at the first occurrence of b'\0'
        terminator_index = response.find(b'\0')
        if terminator_index != -1:
            response_data = response[:terminator_index]
        else:
            response_data = response

        response_str = response_data.decode()

        try:
            json_response = json.loads(response_str)
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
'''


class Server(QObject):
    new_client_connected = Signal(str)

    def __init__(self, host, port):
        super().__init__()
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
            client_hwid = client_socket.recv(1024).decode()
            self.clients[client_name] = client_socket
            print(f"New connection from {client_address} ({client_name}, {client_hwid})")
            self.new_client_connected.emit(client_name)  # Emit signal when a new client connects
            self.send_commands(client_socket, client_name, client_hwid)
        except Exception as e:
            print(f"Connection to {client_address} lost: {e}")
        finally:
            self.cleanup_client(client_socket, client_name)

    def send_commands(self, client_socket, client_name, client_hwid):
        commands = ["get_group", "cpu_ram", "power", "battery", "system_info", "processes", "network_data",
                    "storage_info", "sensor_data", "io", "if_addr", "connects", "is_in_domain", "fetch_all_user_info"]
        while True:
            print(f"list of clients: {self.clients}")
            for command in commands:
                try:
                    time.sleep(1)
                    self.send_command(client_socket, command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received, client_hwid))
                except Exception as e:
                    print(f"Error handling command {command} for {client_name}: {e}")

    def send_command(self, client_socket, command):
        full_command = command.encode() + b"\1"
        client_socket.sendall(full_command)
        print(f"Sent command to client: {command}")

    def receive_response(self, client_socket):
        response = bytearray()
        while True:
            chunk = client_socket.recv(self.chunk_size)
            if not chunk:
                raise ConnectionError("Connection closed by client")

            response.extend(chunk)

            # Check if the terminator is in the received chunk
            if b'\0' in chunk:
                break

        # Split the response at the first occurrence of b'\0'
        terminator_index = response.find(b'\0')
        if terminator_index != -1:
            response_data = response[:terminator_index]
        else:
            response_data = response

        response_str = response_data.decode()

        try:
            json_response = json.loads(response_str)
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
