import socket
import json
import os
import rsa
import wmi
from hardware import ps
from printer import printer
from update import updates
from time import sleep

class Client:
    def __init__(self):
        self.buffer_size = 5120
        self.public_key, self.private_key = rsa.newkeys(2048)  # Increased key size for better security
        self.settings = self.load_settings()
        self.client_socket = None
        self.partner_public_key = None
        self.connect()

    def load_settings(self):
        if not os.path.exists("settings.json"):
            ip = input("Enter IP Address: ")
            port = input("Enter port:")
            settings = {"ip": ip, "port": port}
            with open('settings.json', 'w') as file:
                json.dump(settings, file)
        else:
            with open("settings.json", 'r') as file:
                settings = json.load(file)
        return settings

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.settings['ip'], int(self.settings['port'])))
            self.partner_public_key = rsa.PublicKey.load_pkcs1(self.client_socket.recv(self.buffer_size))
            self.client_socket.send(self.public_key.save_pkcs1("PEM"))
            hwid = self.get_hwid()
            self.send_msg(hwid)
            print("Connected to the server")
        except socket.error as e:
            print(f"Unable to connect to the server: {e}")
            self.reconnect()

    def get_hwid(self):
        c = wmi.WMI()
        hwid = None
        for system in c.Win32_ComputerSystemProduct():
            hwid = system.UUID
        return hwid

    def send_msg(self, message):
        # Assuming `r.send_msg` can handle sending JSON strings.
        r.send_msg(message, self.client_socket, self.partner_public_key)

    def listen(self):
        try:
            while True:
                server_response = r.rcv_msg(self.client_socket, self.private_key)
                if server_response == 'ping':
                    self.send_msg('pong')
                elif server_response == '1':
                    ps.execute_powershell_script(self.client_socket, self.partner_public_key)
                elif server_response == '2':
                    updates.check_updates(self.client_socket, self.partner_public_key)
                elif server_response == '3':
                    printer.list_installed_printers(self.client_socket, self.partner_public_key)
                elif server_response == '0':
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
            self.reconnect()

    def reconnect(self):
        attempts = 0
        while attempts < 5:
            try:
                print(f"Connection lost... Attempting to reconnect ({attempts + 1}/5)")
                self.client_socket = socket.socket()
                self.client_socket.connect((self.settings['ip'], int(self.settings['port'])))
                self.partner_public_key = rsa.PublicKey.load_pkcs1(self.client_socket.recv(self.buffer_size))
                self.client_socket.send(self.public_key.save_pkcs1("PEM"))
                print("Reconnection successful")
                return
            except socket.error:
                attempts += 1
                sleep(2)
        print("Failed to reconnect after 5 attempts")
        self.close()

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")

if __name__ == '__main__':
    client = Client()
    client.listen()
    client.close()
