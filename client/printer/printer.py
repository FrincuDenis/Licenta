import time
import win32print
import winreg
from client import rcv
buffer_size=1024
def get_printer_ip(printer_name,client_socket,public_key):
    try:
        # Open the registry key where printer port information is stored
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Print\Printers')

        # Iterate through the printer subkeys and find the one matching the printer name
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            if subkey_name.startswith(printer_name):
                port_key = winreg.OpenKey(key, subkey_name)
                # Get the Port value, which contains the IP address or hostname
                port_value, _ = winreg.QueryValueEx(port_key, 'Port')
                winreg.CloseKey(port_key)
                return port_value
    except Exception as e:
        message = f"Error: {e}"
        rcv.send_msg(message, client_socket, public_key)
    return None
def list_installed_printers(client_socket,public_key):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    if printers:
        rcv.send_msg('List of Installed Printers:', client_socket, public_key)
        for printer in printers:
            printer_name = printer[2]
            printer_ip = get_printer_ip(printer_name,client_socket,public_key)
            if printer_ip:
                message= f"- {printer_name} [{printer_ip}]\n"
                rcv.send_msg(message, client_socket, public_key)
                time.sleep(0.15)
            else:
                message= f"- {printer_name} [IP not found]"
                rcv.send_msg(message, client_socket, public_key)
    else:
        rcv.send_msg('No printers found.', client_socket, public_key)
    time.sleep(0.2)
    rcv.send_msg('0', client_socket, public_key)