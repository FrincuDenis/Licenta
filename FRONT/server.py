import socket
import time


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")

        client_socket, client_address = self.server_socket.accept()
        print(f"Connected to client at {client_address}")

        while True:
            # Accept input from the user
            print(
                "Options:\n1.cpu&ram\n2.power\n3.battery\n4.system_info\n5.processes\n6.network_data\n7.storage_info\n8.sensor_data")
            command = input("Enter command for client: ")
            if command:
                if command == "1":
                    client_socket.sendall(b"cpu_ram")
                elif command == "2":
                    client_socket.sendall(b"power")
                elif command == "3":
                    client_socket.sendall(b"battery")
                elif command == "4":
                    client_socket.sendall(b"system_info")
                elif command == "5":
                    client_socket.sendall(b"processes")
                elif command == "6":
                    client_socket.sendall(b"network_data")
                elif command == "7":
                    client_socket.sendall(b"storage_info")
                elif command == "8":
                    client_socket.sendall(b"sensor_data")
                print("Command sent to client.")

                # Receive response from client in chunks
                response = self.receive_chunks(client_socket)
                if response:
                    # Process the received response
                    self.process_response(response)
                    print("Response received from client.")
                else:
                    print("No response received from client.")
            else:
                print("Command was not sent.")

        client_socket.close()

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


if __name__ == "__main__":
    server = Server("localhost", 8080)
    server.start()
