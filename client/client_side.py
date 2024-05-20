import socket
import json
import os
import time

import rsa
import wmi
import rcv as r
from hardware import ps
from printer import printer
from update import updates
from time import sleep

buffer_size = 5120
public_key, private_key = rsa.newkeys(2048)  # Increased key size for better security

def get_hwid():
    c = wmi.WMI()
    hwid = None
    for system in c.Win32_ComputerSystemProduct():
        hwid = system.UUID
    return hwid

def load_settings():
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

def reconnect(host, port):
    attempts = 0
    while attempts < 5:
        try:
            print(f"Connection lost... Attempting to reconnect ({attempts + 1}/5)")
            client_socket = socket.socket()
            client_socket.connect((host, port))
            partner_public_key = rsa.PublicKey.load_pkcs1(client_socket.recv(buffer_size))
            client_socket.send(public_key.save_pkcs1("PEM"))
            print("Reconnection successful")
            return client_socket, partner_public_key
        except socket.error:
            attempts += 1
            sleep(2)
    print("Failed to reconnect after 5 attempts")
    return None, None

settings = load_settings()
host, port = settings['ip'], int(settings['port'])

client_socket = None
partner = None

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    partner = rsa.PublicKey.load_pkcs1(client_socket.recv(buffer_size))
    client_socket.send(public_key.save_pkcs1("PEM"))
    hwid = get_hwid()
    r.send_msg(hwid, client_socket, partner)
    print("Connected to the server")
    time.sleep(10)
    while True:
        server_response = r.rcv_msg(client_socket, private_key)
        if server_response == 'ping':
            r.send_msg('pong', client_socket, partner)
        elif server_response == '1':
            ps.execute_powershell_script(client_socket, partner)
        elif server_response == '2':
            updates.check_updates(client_socket, partner)
        elif server_response == '3':
            printer.list_installed_printers(client_socket, partner)
        elif server_response == '0':
            break

except socket.error as e:
    print(f"Socket error occurred: {e}")
    client_socket, partner = reconnect(host, port)
    if client_socket is None:
        print("Unable to reconnect and terminating.")
except Exception as e:
    print(f"An error occurred: {e}")

if client_socket:
    client_socket.close()


# Close the client socket when exiting
client_socket.close()
# TODO: 1.sa salvezi clienti in baza de date si sa fie identificati pe baza de hashului dat de HWID si sa aiba cheia publica
#  2.sa poti selecta clienti ex: vreau sa selectez clientul 5
#  3.sa poti executa o comanda simultan pe mai multi clienti pe toti odata sau sa alegi despartiti prin virgula ex: 2,3,10,24 sau all
#  4.sa implementam sa putem rula mai multe comenzi ex: harware_info,update,printer etc
#  5.in teste e un fisier consola pe ala il faci pt sa trimita catre client comenzi iar clientu sa execute comenzile in cmd:regedit;ipconfig,diskpart etc
#   6. notificare update