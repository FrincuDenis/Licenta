import subprocess
import json
import os
import wmi
import csv
import sys
import string
import ctypes
import win32api

#fisier principal pt stick
def get_serial_number():
    try:
        c = wmi.WMI()
        for bios in c.Win32_BIOS():
            serial_number = bios.SerialNumber.strip()
            if serial_number:
                return serial_number
    except Exception as e:
        print("An error occurred:", e)
    return None
def get_system_info():
    try:
        c = wmi.WMI()
        # Query the Win32_ComputerSystem class to get system information
        system_info = c.Win32_ComputerSystem()[0]
        # Extract the manufacturer and model properties
        manufacturer = system_info.Manufacturer
        model = system_info.Model
        return manufacturer, model
    except Exception as e:
        print("An error occurred:", e)
        return None, None
def get_system_sku():
    try:
        # Execute the PowerShell command
        command = "powershell.exe -Command \"(Get-CimInstance -Namespace root\wmi -ClassName MS_SystemInformation).SystemSKU\""
        output = subprocess.check_output(command, shell=True)
        # Decode the output to string format
        output_str = output.decode("utf-8").strip()
        return output_str
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None
#fosta functie pt ps
def execute_powershell_script1(filename):
    filename += '.csv'
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

        result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            error_message = f"PowerShell script execution failed with error: {result.stderr}"
            print(error_message)
        else:
            output_message = result.stdout
            print(output_message)

            # Deserialize JSON output
            final_json = json.loads(output_message)

            # Add serial number to JSON data
            serial_number = get_serial_number()
            sku = get_system_sku()
            manufacture,model=get_system_info()
            final_json['Manufacture']=manufacture
            final_json['Model'] = model
            final_json['Serial Number'] = serial_number
            final_json['System SKU'] = sku
            # Save JSON data to a CSV file
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = final_json.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the CSV file is empty and write the header if needed
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(final_json)
                print(f"JSON data saved to {filename}")

    except Exception as e:
        error_message = f"An error occurred while running PowerShell script: {e}"

def execute_powershell_script(filename, volume):
    filename += '.csv'
    try:
        usb_drive_letter = volume
        if usb_drive_letter:
            csv_file_path = os.path.join(volume, filename)
            '''
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            powershell_script = os.path.join(bundle_dir, "client.ps1")
            '''
            current_directory = os.path.dirname(os.path.abspath(__file__))
            powershell_script_path = os.path.join(current_directory, 'client.ps1')

            with open(powershell_script_path, 'r', encoding='utf-8') as script_file:
                powershell_script = script_file.read()
            result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', powershell_script],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                error_message = f"PowerShell script execution failed with error: {result.stderr}"
                print(error_message)
            else:
                output_message = result.stdout
                print(output_message)

                final_json = json.loads(output_message)

                serial_number = get_serial_number()
                sku = get_system_sku()
                manufacture, model = get_system_info()
                final_json['Manufacture'] = manufacture
                final_json['Model'] = model
                final_json['Serial Number'] = serial_number
                final_json['System SKU'] = sku

                with open(csv_file_path, 'a', newline='') as csvfile:
                    fieldnames = final_json.keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if csvfile.tell() == 0:
                        writer.writeheader()

                    writer.writerow(final_json)
                    print(f"JSON data saved to {csv_file_path}")
        else:
            print("USB drive not found.")

    except Exception as e:
        error_message = f"An error occurred while running PowerShell script: {e}"

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: ps2.exe <arg1> <arg2>")
        return

    # Access the arguments
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    # Use the arguments
    print("Argument 1:", arg1)
    print("Argument 2:", arg2)

    execute_powershell_script(arg1,arg2)

if __name__ == "__main__":
    main()

