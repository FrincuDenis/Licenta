import json
import os
import subprocess
import time
from sys import path
from client import rcv
json_data={}
buffer_size=1024
#functie pt client
def execute_powershell_script(client_socket,public_key):
    #powershell_script = pkgutil.get_data(__name__, 'client.ps1').decode('utf-8')
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
            rcv.send_msg(message,client_socket,public_key)
        else:
            if result.stdout:
                # Serialize the result.stdout into JSON
                json_data = json.loads(json.dumps(result.stdout))
                items = json_data.split('\n')
                # Send the JSON result to the server in chunks (buffers)
                for item in items:
                    if item.strip():  # Skip empty lines
                        try:
                            rcv.send_msg(item, client_socket, public_key)
                            time.sleep(0.2)
                        except Exception as e:
                                message = f"An error occurred while running PowerShell script: {e}"
                                rcv.send_msg(message, client_socket, public_key)
                rcv.send_msg('0', client_socket, public_key)


    except Exception as e:
        message = f"An error occurred while running PowerShell script: {e}"
        rcv.send_msg(message, client_socket, public_key)