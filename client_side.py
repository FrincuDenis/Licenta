import socket
import subprocess
import json
import time
import win32print
import winreg
import win32com.client
import os
import pkgutil
# Define the server IP and port
SERVER_IP = '172.29.2.11'
SERVER_PORT = 4445

#SERVER_IP = 'localhost'
#SERVER_PORT = 8888
buffer_size=1024
message=""
max_attempts=5
connected = False
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def get_printer_ip(printer_name):
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
def list_installed_printers():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    if printers:
        client_socket.send(b'List of Installed Printers:')
        for printer in printers:
            printer_name = printer[2]
            printer_ip = get_printer_ip(printer_name)
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
def download_and_install_updates(updates_to_install):
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
         # Create a Windows Update Downloader object
            update_downloader = update_session.CreateUpdateDownloader()
            update_downloader.Updates = updates_to_install

            client_socket.send(b'Downloading updates...')
            download_result = update_downloader.Download()

            if download_result.ResultCode == 2:
                client_socket.send(b'Downloaded updates successfully.')
            else:
                client_socket.send(b'Failed to download updates.')
                return

            # Create a Windows Update Installer object
            installer = update_session.CreateUpdateInstaller()
            installer.Updates = updates_to_install
            client_socket.send(b'Installing updates...')
            installation_result = installer.Install()

            for i, update in enumerate(updates_to_install):
                message=f"Installing update {i + 1}: {update.Title}"
                client_socket.send(message.encode())
            if installation_result.ResultCode == 2:
                client_socket.send(b'Installed updates successfully.')
            else:
                client_socket.send(b'Failed to install updates.')
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        client_socket.send(message.encode())
        client_socket.send(b'0')

def check_updates():
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
        client_socket.send(b'Searching for updates...')
        search_result = update_searcher.Search("IsInstalled=0 and Type='Software'")

        # Check if updates are available
        if search_result.Updates.Count > 0:
            message= f"Found {search_result.Updates.Count} updates."
            client_socket.send(message.encode())
            updates_to_install = search_result.Updates

            # Display the list of updates
            client_socket.send(b'List of updates:')
            for i, update in enumerate(updates_to_install):
                message=f"{i + 1}. {update.Title} "
                client_socket.send(message.encode())
        client_socket.send(b'Want to install updates?')
        time.sleep(0.2)
        client_socket.send(b'1.Yes')
        time.sleep(0.2)
        client_socket.send(b'2.No(return to meniu)')
        time.sleep(0.2)
        client_socket.send(b'rasp')
        rasp=client_socket.recv(buffer_size).decode()
        if rasp == '1':
            download_and_install_updates(updates_to_install)
        else:
            client_socket.send(b'0')
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        client_socket.send(message.encode())
        client_socket.send(b'0')
        print(f"An error occurred: {str(e)}")

def execute_powershell_script():
    #powershell_script = pkgutil.get_data(__name__, 'powershell.ps1').decode('utf-8')
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the path to your PowerShell script (assuming it's in the same folder)
    powershell_script_path = os.path.join(current_directory, 'client.ps1')

    # Read the content of the PowerShell script
    with open(powershell_script_path, 'r', encoding='utf-8') as script_file:
        powershell_script = script_file.read()
    try:
        result = subprocess.run(['powershell', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            message=f"PowerShell script execution failed with error: {result.stderr}"
            client_socket.send(message.encode())
        else:
            message=result.stdout
            client_socket.send(message.encode())

        if result.stdout:
            # Serialize the result.stdout into JSON
            json_data = json.dumps(result.stdout)
            # Send the JSON result to the server in chunks (buffers)
            for i in range(0, len(json_data), buffer_size):
                client_socket.send(json_data[i:i + buffer_size].encode())
            client_socket.send(b'0')


    except Exception as e:
        message = f"An error occurred while running PowerShell script: {e}"
        client_socket.send(message.encode())

def reconnect():
    global connected
    attempts = 0
    while attempts < max_attempts:
        if not connected:
            try:
                # Attempt to reconnect to the server
                client_socket.connect((SERVER_IP, SERVER_PORT))
                print("Reconnected to the server")
                connected = True
                return True
            except ConnectionRefusedError:
                attempts += 1
                print(f"Connection attempt {attempts}/{max_attempts} failed. Server may be offline.")
                if attempts == max_attempts:
                    print("Server is offline. Unable to establish a connection.")
                    return False
                time.sleep(5)  # Wait for a moment before retrying
        else:
            # If already connected, no need to reconnect
            return True
    return False


if __name__ == '__main__':
    while True:
        try:
            if not connected:
                # Attempt to connect to the server if not already connected
                client_socket.connect((SERVER_IP, SERVER_PORT))
                connected = True
                print("Connected to the server")

            while True:
                server_response = client_socket.recv(buffer_size).decode()
                if not server_response:
                    # Server has closed the connection or signaled the end
                    break
                if server_response == '1':
                    execute_powershell_script()
                elif server_response == '2':
                    check_updates()
                elif server_response == '3':
                    list_installed_printers()
                elif server_response == '0':
                    client_socket.close()
        except ConnectionResetError:
            print("Connection to the server was forcibly closed.")
            connected = False  # Reset the connection status
        except ConnectionRefusedError:
            print("Server is offline. Attempting to reconnect...")
            if not reconnect():
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # Close the client socket when exiting
    client_socket.close()

