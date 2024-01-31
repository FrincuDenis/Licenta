import subprocess
import json
import os
import wmi
import csv
import sys
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

def execute_powershell_script(filename):
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
            final_json['Serial Number'] = serial_number

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

def main():
    filename = input("Enter filename: ")
    try:
        execute_powershell_script(filename)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
