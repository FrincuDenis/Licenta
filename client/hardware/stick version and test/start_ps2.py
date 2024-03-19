import os
import shutil
import json
import subprocess
import sys
#start fisier principal
def main():
    try:
        current_script_path = os.path.abspath(sys.executable)
        drive_letter = os.path.splitdrive(current_script_path)[0]

        if not os.path.exists("settings.json"):
            filename = input("Enter filename: ")
            settings = {"filename": filename}
            with open('settings.json', 'w') as file:
                json.dump(settings, file)
        else:
            while(True):
                print("Want to keep the settings file? (Y): " )
                answer = input()
                print(answer)
                if answer == "Y" or answer == "y" or not answer.strip():
                    with open("settings.json", 'r') as file:
                        settings = json.load(file)
                    break
                elif answer == "N" or answer == "n":
                    filename = input("Enter filename: ")
                    settings = {"filename": filename}
                    with open('settings.json', 'w') as file:
                        json.dump(settings, file)
                    break
                else:
                    print("Invalid option.Use this options:(Y/y)es or enter,(N/n)o,")
        start_script_dir = os.path.dirname(os.path.abspath(sys.executable))
        usb_ps2_path = os.path.join(start_script_dir, 'ps2_stick.exe')  # Specify the path to ps2.exe on the USB stick
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        shutil.copy(usb_ps2_path, desktop_path)

        # Run ps2.exe with loaded arguments
        ps2_path = os.path.join(desktop_path, 'ps2_stick.exe')
        command = [ps2_path, settings['filename'], drive_letter]
        print('Script running')
        # Run the command and capture the output
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Get the captured output
        output = completed_process.stdout
        error_output = completed_process.stderr

        # Check if the command was successful
        if completed_process.returncode == 0:
            print("Command executed successfully.")
            print("Output:", output)
        else:
            print("Error executing command.")
            print("Error output:", error_output)

        # Delete ps2.exe after it finishes
        os.remove(ps2_path)

    except Exception as e:
        print("Error:", str(e))  # Convert exception to string for printing
        input("Press ANY KEY")

if __name__ == "__main__":
    main()
