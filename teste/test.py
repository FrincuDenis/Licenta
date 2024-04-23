import socket
import rsa

def load_key():
    with open('client_private_key.pem', 'rb') as f:
        priv_key = rsa.import_key(f.read())
    return priv_key

def handle_server(server_socket):
    priv_key = load_key()

    # Primiți cheia publică a serverului
    server_public_key = server_socket.recv(1024)
    server_key = rsa.import_key(server_public_key)

    while True:
        try:
            # Primiți mesajul criptat de la server
            encrypted_data = server_socket.recv(1024)
            if not encrypted_data:
                break

            # Decriptați mesajul folosind cheia privată a clientului
            decrypted_data = rsa.decrypt(encrypted_data, priv_key)
            message = decrypted_data.decode('utf-8')

            # Afișați mesajul primit de la server
            print(f"[SERVER] {message}")

            # Introduceți input de la client
            client_input = input("Introduceți răspunsul: ")

            # Criptați inputul de la client folosind cheia publică a serverului
            encrypted_client_input = rsa.encrypt(client_input.encode('utf-8'), server_key)

            # Trimiteți inputul criptat de la client către server
            server_socket.sendall(encrypted_client_input)

        except:
            break

    server_socket.close()

HOST = 'localhost'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

handle_server(client_socket)
