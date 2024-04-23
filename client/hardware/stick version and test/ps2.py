import subprocess
import json
import os
import socket
import sys
# pentru a executa din executabil si a a se conecta la server
def execute_powershell_script(client_socket):
    buffer_size = 1024
    try:
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

        # Specify the path to your embedded PowerShell script
        powershell_script = os.path.join(bundle_dir, "client.ps1")
        '''
        current_directory = os.path.dirname(os.path.abspath(__file__))
        powershell_script_path = os.path.join(current_directory, 'client.ps1')

        with open(powershell_script_path, 'r', encoding='utf-8') as script_file:
            powershell_script = script_file.read()
        '''
        result = result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            error_message = f"PowerShell script execution failed with error: {result.stderr}"
            client_socket.send(error_message.encode())
        else:
            output_message = result.stdout
            client_socket.send(output_message.encode())

            # Serialize the result.stdout into JSON
            json_data = json.dumps(result.stdout)

            # Send the JSON result to the server in chunks (buffers)
            for i in range(0, len(json_data), buffer_size):
                client_socket.send(json_data[i:i + buffer_size].encode())

            # Send an end-of-transmission signal
            client_socket.send(b'0')

    except Exception as e:
        error_message = f"An error occurred while running PowerShell script: {e}"
        client_socket.send(error_message.encode())
    finally:
        client_socket.close()

def main():
    buffer_size = 5120
    if not os.path.exists("settings.json"):
        ip = input("Enter IP Address: ")
        port = input("Enter port: ")
        settings = {"ip": ip, "port": port}
        with open('settings.json', 'w') as file:
            json.dump(settings, file)
    else:
        with open("settings.json", 'r') as file:
            settings = json.load(file)

    host = settings["ip"]
    port = int(settings["port"])
    filename=input("Enter filename: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(filename.encode('utf-8'))
    try:
        execute_powershell_script(client_socket)
    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()

if __name__ == "__main__":
    main()
