import rsa
def send_msg(message, socket, public_key):
    socket.send(rsa.encrypt(message.encode(), public_key))


def rcv_msg(socket, private_key):
    return rsa.decrypt(socket.recv(1024), private_key).decode()
