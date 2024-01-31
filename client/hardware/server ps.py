import json
import csv
import socket
import wmi
def get_serial_number():
    try:
        # Create a WMI object
        c = wmi.WMI()

        # Query the BIOS serial number
        for bios in c.Win32_BIOS():
            serial_number = bios.SerialNumber.strip()
            if serial_number:
                return serial_number

    except Exception as e:
        print("An error occurred:", e)

    return None


# bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# Specify the path to your embedded PowerShell script
# powershell_script = os.path.join(bundle_dir, "client.ps1")

def hardware_info(client_socket,filename):
    print("Gathering hardware information")
    filename+='.csv'
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        print("Received data from client:", data)

        if not data.strip():
            print("Empty data received, skipping processing")
            return

        # Parse the received JSON data
        try:
            json_data = json.loads(data)
            print("Received JSON data:")

            # Get serial number
            serial_number = get_serial_number()

            # Add serial number to JSON data
            json_data['Serial Number'] = serial_number
            print(json.dumps(json_data, indent=2))
            # Save JSON data to a CSV file
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = json_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the CSV file is empty and write the header if needed
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(json_data)
                print(f"JSON data saved to {filename}")
        except (json.JSONDecodeError, ValueError) as e:
            print("Failed to parse JSON data:", e)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

server_address = ('172.29.1.162', 44452)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(0)
print("Server is listening for incoming connections...")
try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        filename=client_socket.recv(1024).decode('utf-8')
        hardware_info(client_socket,filename)
except KeyboardInterrupt:
    print("Server interrupted. Closing server socket.")
    server_socket.close()
