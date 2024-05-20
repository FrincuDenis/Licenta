import socket
import threading
import rsa
from client import rcv as r
def handle_client(client_socket):
    public_key, private_key = rsa.newkeys(1024)
    # Trimiteți cheia publică a serverului către client
    client_socket.send(public_key.save_pkcs1("PEM"))
    partner = client_socket.recv(1024)
    while True:
        try:
            r.send_msg(b"macaroane", client_socket, private_key)
            # Primiți mesajul criptat de la client
            message=r.rcv_msg(client_socket, private_key)

            # Afișați mesajul primit de la client
            print(f"[CLIENT] {message}")

            # Solicitați input de la server
            server_input = input("Introduceți răspunsul: ")

            # Criptați inputul de la client folosind cheia publică a serverului
            r.send_msg(server_input, client_socket, partner)
        except:
            break

    client_socket.close()

HOST = 'localhost'
PORT = 8001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

while True:
    client_socket, address = server.accept()
    print(f"[CONEXIUNE] Conectat la {address}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()