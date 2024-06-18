from PySide2.QtCore import QObject, Signal
import socket
import threading
import json
import time
import db_connect


class Server(QObject):
    new_client_connected = Signal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.command_queue = []
        self.chunk_size = 7196
        self.stop_event = threading.Event()

        # Establish database connection
        self.db_connection = db_connect.conectare_bd(
            host="localhost",
            user="root",
            password="rOOt",
            database="licenta"
        )

    def handle_client(self, client_socket, client_address):
        try:
            client_name = client_socket.recv(1024).decode()
            client_hwid = client_socket.recv(1024).decode()
            self.update_client_status(client_name, client_hwid, client_address, status='connected')
            print(f"New connection from {client_address} ({client_name}, {client_hwid})")
            self.new_client_connected.emit(client_name)  # Emit signal when a new client connects
            self.send_commands(client_socket, client_name, client_hwid)
        except Exception as e:
            print(f"Connection to {client_address} lost: {e}")
        finally:
            self.cleanup_client(client_socket, client_name)

    def update_client_status(self, client_name, client_hwid, client_address, status):
        existing_client = db_connect.selectare_inregistrari(
            self.db_connection, 'client', conditie=f"name='{client_name}'"
        )
        if existing_client:
            db_connect.actualizare_inregistrare(
                self.db_connection, 'client',
                {'hwid': client_hwid, 'address': client_address[0], 'port': client_address[1], 'status': status},
                f"name='{client_name}'"
            )
        else:
            db_connect.adaugare_inregistrare(
                self.db_connection, 'client',
                {'name': client_name, 'hwid': client_hwid, 'address': client_address[0], 'port': client_address[1],
                 'status': status}
            )

    def send_commands(self, client_socket, client_name, client_hwid):
        commands = ["get_group", "is_in_domain", "fetch_all_user_info", "cpu_ram", "power", "battery",
                    "system_info", "processes", "storage_info", "sensor_data", "network_data", "io", "if_addr",
                    "connects", "installed_programs"]
        while not self.stop_event.is_set():
            print(f"list of clients: {self.get_all_clients()}")
            for command in commands:
                if self.stop_event.is_set():
                    break
                try:
                    time.sleep(3)
                    self.send_command(client_socket, command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received, client_hwid))
                except Exception as e:
                    print(f"Error handling command {command} for {client_name}: {e}")

    def send_command(self, client_socket, command):
        full_command = command.encode() + b"\1"
        client_socket.sendall(full_command)

    def receive_response(self, client_socket):
        response = bytearray()
        while not self.stop_event.is_set():
            chunk = client_socket.recv(self.chunk_size)
            if not chunk:
                raise ConnectionError("Connection closed by client")

            response.extend(chunk)

            if b'\0' in chunk:
                break

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
        client_socket = self.get_client_socket(name)
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
        self.update_client_status(client_name, None, (None, None), status='disconnected')
        print(f"Client {client_name} has been disconnected and status updated.")

    def get_all_clients(self):
        return db_connect.selectare_inregistrari(self.db_connection, 'client')

    def get_client_socket(self, client_name):
        client = db_connect.selectare_inregistrari(self.db_connection, 'client',
                                                   conditie=f"name='{client_name}' AND status='connected'")
        if client:
            client_address = (client[0][3], int(client[0][4]))
            return socket.create_connection(client_address)
        return None

    def stop(self):
        self.stop_event.set()
        self.server_socket.close()
        print("Server stopped")

    def start(self):
        print(f"Server started at {self.host}:{self.port}")
        try:
            while not self.stop_event.is_set():
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except (KeyboardInterrupt, OSError):
            self.stop()

if __name__ == "__main__":
    server = Server("localhost", 9000)
    server.start()
