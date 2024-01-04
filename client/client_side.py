from hardware import ps
from printer import printer
from update import updates
import socket
import json
from time import sleep
import os
import rsa
public_key, private_key = rsa.newkeys(1024)
partner=None
recpassed=None
if not os.path.exists("settings.json"):
    file = open('settings.json', 'a')
    ip = input("Enter IP Address: ")
    port = input("Enter port:")
    settingsW = {"ip": ip, "port": port}
    file.write(json.dumps(settingsW))
else:
    file = open("settings.json", 'r')
load = json.loads(file.read())
host = load["ip"]
port = int(load["port"])
buffer_size=5120
def send_msg(message,socket,public_key):
    socket.send(rsa.encrypt(message.encode(), public_key))
def rcv_msg(socket,private_key):
    rsa.decrypt(socket.recv(buffer_size), private_key).decode()
def reconnect(host,port):
    reconnect=True
    error=0
    attempts=0
    while reconnect:
        # set connection status and recreate socket
        connected = False
        clientSocket = socket.socket()
        print("connection lost... reconnecting")
        while not connected :
            # attempt to reconnect, otherwise sleep for 2 seconds
            try:
                print(f"Attempting {attempts} times from 5")
                clientSocket.connect((host, port))
                connected = True
                print("re-connection successful")
                reconnect = False
            except socket.error:
                attempts+=1
                if attempts==5:
                    reconnect = False
                    error=1
                    break
                sleep(2)
    if error==0:
        return clientSocket
    else:
        return False
while True:
    try:
        if not recpassed:
            # Attempt to connect to the server if not already connected
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host,port))
            partner = rsa.PublicKey.load_pkcs1(client_socket.recv(buffer_size))
            client_socket.send(public_key.save_pkcs1("PEM"))
            connected = True
            print("Connected to the server")
        else:
            client_socket=recpassed
        while True:
            server_response = rcv_msg(client_socket,private_key)
            rasp =server_response
            print(rasp)
            if not server_response == b'':
                if server_response == '1':
                    ps.execute_powershell_script(client_socket,partner)
                elif server_response == '2':
                    updates.check_updates(client_socket,partner)
                elif server_response == '3':
                    printer.list_installed_printers(client_socket,partner)
                elif server_response == '0':
                    client_socket.close()
    except Exception as e:
            print(f"An error occurred: {e}")
            recpassed=reconnect(host,port)
            if recpassed:
                 pass
            else:
                print(f"Coudn't connect to the server!")
                break
# Close the client socket when exiting
client_socket.close()

