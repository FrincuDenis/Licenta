import os
import shutil
import glob

def get_usb_drive_letter():
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    available_drives = [d for d in drives if os.path.exists(d)]
    for drive in available_drives:
        drive_type = GetDriveType(drive)
        if drive_type == DRIVE_REMOVABLE:
            return drive
    return None

def get_file_path_on_usb(file_name):
    usb_drive_letter = get_usb_drive_letter()
    if usb_drive_letter:
        file_path = os.path.join(usb_drive_letter, file_name)
        if os.path.exists(file_path):
            return file_path
    return None

def copy_file_from_usb(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
        print("File copied successfully.")
    except Exception as e:
        print("Error:", e)

def execute_file(file_path):
    try:
        os.system(file_path)
        print("File executed successfully.")
    except Exception as e:
        print("Error:", e)

def move_file_to_usb(source_path, usb_drive_letter):
    try:
        destination_path = os.path.join(usb_drive_letter, os.path.basename(source_path))
        shutil.move(source_path, destination_path)
        print("File moved to USB stick successfully.")
    except Exception as e:
        print("Error:", e)

def delete_file(file_path):
    try:
        os.remove(file_path)
        print("File deleted successfully.")
    except Exception as e:
        print("Error:", e)

def main():
    csv_name=input("Name csv: ")
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # Detect test.exe file on USB
    usb_test_exe_path = get_file_path_on_usb("ps2_stick_model_and_manufacturer.exe")
    if not usb_test_exe_path:
        print("ps2_stick_model_and_manufacturer.exe file not found on USB.")
        return

    # Copy test.exe file from USB to desktop
    copy_file_from_usb(usb_test_exe_path, desktop_path)

    # Execute test.exe from desktop
    desktop_test_exe_path = os.path.join(desktop_path, "ps2_stick_model_and_manufacturer.exe")
    execute_file(desktop_test_exe_path)

    # Detect a.csv file on desktop
    desktop_csv_path = os.path.join(desktop_path, csv_name)
    if not os.path.exists(desktop_csv_path):
        print(f"{csv_name} file not found on desktop.")
        return

    # Move a.csv file to USB
    usb_drive_letter = os.path.splitdrive(usb_test_exe_path)[0]
    move_file_to_usb(desktop_csv_path, usb_drive_letter)

    # Delete test.exe and a.csv files from desktop
    delete_file(desktop_test_exe_path)
    delete_file(desktop_csv_path)

if __name__ == "__main__":
    main()
