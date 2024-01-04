import socket
import socket

import rsa

public_key, private_key = rsa.newkeys(1024)
partner=None
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("Server is listening for connections...")
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

conn.send(public_key.save_pkcs1("PEM"))
partner = rsa.PublicKey.load_pkcs1(conn.recv(1024))

while True:
    print("Partner: " + rsa.decrypt(conn.recv(1024), private_key).decode())
conn.close()
server_socket.close()




