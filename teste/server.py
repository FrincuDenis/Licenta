import os
import socket
import csv
from datetime import datetime, timedelta
import threading
import time
import shutil

# Define server parameters
HOST = '127.0.0.1'  # localhost
PORT = 65432  # Arbitrary non-privileged port

# Lock for thread-safe access to CSV file
csv_lock = threading.Lock()


def handle_client(conn, addr):
    print('Connected by', addr)



    #print(f'Received and saved: Timestamp={timestamp}, CPU={cpu_value}, GPU={gpu_value}')

    conn.close()





def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print('Server is listening...')

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == '__main__':
    server_thread = threading.Thread(target=main)
    server_thread.start()
    calculate_average()
    server_thread.join()
