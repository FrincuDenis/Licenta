import subprocess
import json
import os
import pkgutil
buffer_size=1024
def execute_powershell_script(client_socket):
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