import socket
import threading
import datetime
import platform
import json


def get_system_info():
    system_info = {
        "time": datetime.datetime.now().strftime("%I:%M:%S %p"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "machine": platform.machine(),
        "version": platform.version(),
        "platform": platform.platform(),
        "system": platform.system(),
        "processor": platform.processor()
    }
    return system_info


def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    if request == "GET_SYSTEM_INFO":
        info = get_system_info()
        response = json.dumps(info)
        client_socket.send(response.encode('utf-8'))
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
