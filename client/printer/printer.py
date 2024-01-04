import time
import win32print
import winreg
buffer_size=5120
def get_printer_ip(printer_name,client_socket):
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
        client_socket.send(message.encode())
    return None
def list_installed_printers(client_socket):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    if printers:
        client_socket.send(b'List of Installed Printers:')
        for printer in printers:
            printer_name = printer[2]
            printer_ip = get_printer_ip(printer_name,client_socket)
            if printer_ip:
                message= f"- {printer_name} [{printer_ip}]\n"
                client_socket.send(message.encode())
            else:
                message= f"- {printer_name} [IP not found]"
                client_socket.send(message.encode())
    else:
        client_socket.send(b'No printers found.')
    time.sleep(0.2)
    client_socket.send(b'0')