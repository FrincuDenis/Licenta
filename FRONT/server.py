from PySide2.QtCore import QObject, Signal
import socket
import threading
import json
import time
import db_connect
import logging
from logging_config import setup_logging


class Server(QObject):
    new_client_connected = Signal(str)

    def __init__(self, host, port, db):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(0)
        self.clients = {}
        self.command_queue = []
        self.chunk_size = 10000
        self.stop_event = threading.Event()
        self.db_connection = db
        self.logger = setup_logging()

    def handle_client(self, client_socket, client_address):
        try:
            client_name = client_socket.recv(1024).decode()
            client_hwid = client_socket.recv(1024).decode()
            self.clients[client_name] = client_socket
            self.update_client_status(client_name, client_hwid, client_address, status='Connected')
            self.logger.info(f"New connection from {client_address} ({client_name}, {client_hwid})")
            self.new_client_connected.emit(client_name)  # Emit signal when a new client connects
            self.send_commands(client_socket, client_name)
        except Exception as e:
            self.logger.error(f"Connection to {client_address} lost: {e}")
        finally:
            self.cleanup_client(client_socket, client_name)

    def update_client_status(self, client_name, client_hwid="", client_address=["", "0"], status="Disconnected"):
        try:
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
        except Exception as e:
            setup_logging().error(f"Error updating client status: {e}")

    def save_client_to_db(self, client_name, client_hwid, client_address):
        try:
            query = "INSERT INTO clients (name, hwid, address) VALUES (%s, %s, %s)"
            params = (client_name, client_hwid, str(client_address))
            self.db_connection.execute(query, params)
            self.db_connection.commit()
            self.logger.info(f"Saved client {client_name} to database.")
        except Exception as e:
            self.logger.error(f"Failed to save client {client_name} to database: {e}")

    def save_command_response_to_db(self, client_name, command, response):
        try:
            query = "INSERT INTO command_responses (client_name, command, response) VALUES (%s, %s, %s)"
            params = (client_name, command, json.dumps(response))
            self.db_connection.execute(query, params)
            self.db_connection.commit()
            self.logger.info(f"Saved command response for {client_name}: {command}")
        except Exception as e:
            self.logger.error(f"Failed to save command response for {client_name}: {e}")

    def send_commands(self, client_socket, client_name):
        commands = ["get_group",  "fetch_all_user_info","is_in_domain", "cpu_ram", "battery", "power",
                    "system_info", "processes", "storage_info", "sensor_data", "network_data", "io", "if_addr",
                    "connects", "installed_programs"]
        while not self.stop_event.is_set():
            for command in commands:
                if self.stop_event.is_set():
                    break
                try:
                    time.sleep(2.5)
                    self.send_command(client_socket, command)
                    command_received, data_received = self.receive_response(client_socket)
                    if command_received:
                        self.command_queue.append((client_name, command_received, data_received))

                except (ConnectionError, socket.error) as e:
                    self.logger.error(f"Error handling command {command} for {client_name}: {e}")
                    self.update_client_status(client_name, status="Disconnected")
                    self.cleanup_client(client_socket, client_name)
                    self.attempt_reconnection(client_name)
                    return


    def send_command(self, client_socket, command):
        full_command = command.encode() + b"\1"
        client_socket.sendall(full_command)
        self.logger.info(f"Sent command to client: {command}")

    def receive_response(self, client_socket):
        response = bytearray()
        while not self.stop_event.is_set():
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
        #(response_str)
        try:
            json_response = json.loads(response_str)
            if isinstance(json_response, dict):
                for command, data in json_response.items():
                    return command, data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")

        return None, None

    def get_next_command(self):
        if self.command_queue:
            return self.command_queue.pop(0)
        return None

    def data_send(self, data, name, command):
        client_socket = self.clients.get(name)
        if not client_socket:
            self.logger.error(f"No client found with name {name}")
            self.update_client_status(name, "", ["", "0"], status="Disconnected")
            return

        data_to_send = json.dumps({command: data})
        for i in range(0, len(data_to_send), self.chunk_size):
            chunk = data_to_send[i:i + self.chunk_size]
            client_socket.sendall(chunk.encode())
        client_socket.sendall(b'\0')
        self.logger.info(f"Command sent to client: {command}")

    def cleanup_client(self, client_socket, client_name):
        client_socket.close()
        if client_name in self.clients:
            del self.clients[client_name]
        self.logger.info(f"Cleaned up client {client_name}")

    def attempt_reconnection(self, client_name):
        max_retries = 5
        retry_delay = 5  # seconds
        for attempt in range(max_retries):
            if self.stop_event.is_set():
                return
            try:
                client_socket = self.clients.get(client_name)
                if client_socket:
                    client_socket.connect((self.host, self.port))
                    self.handle_client(client_socket, (self.host, self.port))
                    return
            except (socket.error, ConnectionError) as e:
                self.logger.error(f"Reconnection attempt {attempt + 1} for {client_name} failed: {e}")
                time.sleep(retry_delay)
        self.logger.error(f"Failed to reconnect to {client_name} after {max_retries} attempts")

    def stop(self):
        self.stop_event.set()
        self.server_socket.close()
        self.logger.info("Server stopped")

    def return_socket(self):
        return self.client_socket
    def start(self):
        self.logger.info(f"Server started at {self.host}:{self.port}")
        try:
            while not self.stop_event.is_set():
                self.client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(self.client_socket, client_address)).start()
        except (KeyboardInterrupt, OSError):
            self.stop()

    def get_all_clients(self):
        try:
            return db_connect.selectare_inregistrari(self.db_connection, 'client')
        except Exception as e:
            setup_logging().error(f"Error getting all clients: {e}")
            return []


if __name__ == "__main__":
    db = db_connect.connect()
    server = Server("localhost", 8080, db)
    server.start()
