import socket
import threading

# Function to handle the forwarding of traffic between client and remote server
def handle_client(client_socket, remote_host, remote_port):
    try:
        # Connect to the remote host
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        # Start threads to forward traffic in both directions
        threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket)).start()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

# Function to forward traffic between two sockets
def forward(source_socket, destination_socket):
    while True:
        try:
            data = source_socket.recv(4096)
            if len(data) == 0:
                break
            destination_socket.send(data)
        except:
            break
    source_socket.close()
    destination_socket.close()

def start_server(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)
    print(f"[*] Listening on {local_host}:{local_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        handle_client(client_socket, remote_host, remote_port)

if __name__ == "__main__":
    local_host = "0.0.0.0"  # Listen on all interfaces
    local_port = 9999       # Local port to listen on
    remote_host = "www.example.com"  # Remote host to forward traffic to
    remote_port = 80        # Remote port to forward traffic to

    start_server(local_host, local_port, remote_host, remote_port)
