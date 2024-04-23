import socket
import threading
import rsa

def generate_keys():
    (pub_key, priv_key) = rsa.generate_public_key(512)
    with open('server_public_key.pem', 'wb') as f:
        f.write(pub_key.export_key())
    with open('server_private_key.pem', 'wb') as f:
        f.write(priv_key.export_key())

def load_keys():
    with open('server_public_key.pem', 'rb') as f:
        pub_key = rsa.import_key(f.read())
    with open('server_private_key.pem', 'rb') as f:
        priv_key = rsa.import_key(f.read())
    return pub_key, priv_key

def handle_client(client_socket):
    pub_key, priv_key = load_keys()

    # Trimiteți cheia publică a serverului către client
    client_socket.sendall(pub_key.export_key())

    while True:
        try:
            # Primiți mesajul criptat de la client
            encrypted_data = client_socket.recv(1024)
            if not encrypted_data:
                break

            # Decriptați mesajul folosind cheia privată a serverului
            decrypted_data = rsa.decrypt(encrypted_data, priv_key)
            message = decrypted_data.decode('utf-8')

            # Afișați mesajul primit de la client
            print(f"[CLIENT] {message}")

            # Solicitați input de la server
            server_input = input("Introduceți răspunsul: ")

            # Criptați inputul de la server folosind cheia publică a clientului
            # (trebuie să obțineți cheia publică a clientului de la client)
            # ... (implementați codul pentru criptarea cu cheia publică a clientului)

            # Trimiteți inputul criptat de la server către client
            # ... (implementați codul pentru trimiterea datelor criptate)

        except:
            break

    client_socket.close()

HOST = 'localhost'
PORT = 8000

generate_keys()  # Generați chei RSA dacă nu există deja

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

while True:
    client_socket, address = server.accept()
    print(f"[CONEXIUNE] Conectat la {address}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()