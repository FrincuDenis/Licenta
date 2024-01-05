
import socket
import rsa
partner = None

public_key, private_key = rsa.newkeys(1024)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

partner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
client_socket.send(public_key.save_pkcs1("PEM"))

while True:
    message = input("Scrie: ")
    client_socket.send(rsa.encrypt(message.encode(), partner))
    print("You: " + message)


