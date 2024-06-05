import socket
import time

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

