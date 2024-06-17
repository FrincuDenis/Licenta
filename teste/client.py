import socket
import subprocess

CHUNK_SIZE = 4096
END_OF_MESSAGE = b'<<END_OF_MESSAGE>>'


def run_powershell_command(command):
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Command failed with error: {result.stderr}"
    return result.stdout


def set_execution_policy():
    return run_powershell_command("Set-ExecutionPolicy -ExecutionPolicy Bypass -Force")


def is_module_installed(module_name):
    return module_name in run_powershell_command(f"Get-Module -ListAvailable -Name {module_name}")


def register_psgallery():
    return run_powershell_command("Register-PSRepository -Default")


def is_psgallery_registered():
    return "PSGallery" in run_powershell_command("Get-PSRepository")


def install_module(module_name):
    command = f"Install-Module -Name {module_name} -Force" if module_name == "PSWindowsUpdate" else f"Install-PackageProvider -Name {module_name} -MinimumVersion 2.8.5.201 -Force"
    return run_powershell_command(command)


def import_module(module_name):
    return run_powershell_command(f"Import-Module -Name {module_name}")


def ensure_prerequisites():
    ps_module = "PSWindowsUpdate"
    nu_module = "NuGet"
    try:
        if not is_module_installed(ps_module):
            set_execution_policy()
            if not is_module_installed(nu_module):
                install_module(nu_module)
            if not is_psgallery_registered():
                register_psgallery()
            if not is_module_installed("PowerShellGet"):
                install_module("PowerShellGet")
            install_module(ps_module)
            import_module(ps_module)
    except Exception as e:
        return f"Failed to ensure prerequisites: {e}"
    return "All prerequisites are met."


def handle_client_command(command):
    prerequisite_check = ensure_prerequisites()
    if "Failed" in prerequisite_check:
        return prerequisite_check

    args = command.split()
    if command == "check-updates":
        return run_powershell_command("Get-WindowsUpdate")
    elif command == "install-updates":
        return run_powershell_command("Install-WindowsUpdate -AcceptAll -AutoReboot")
    elif args[0] == "hide-update":
        return run_powershell_command(f"Hide-WindowsUpdate -KBArticleID {args[1]} -Verbose")
    elif args[0] == "schedule-update":
        update_id, revision, hour, minute = args[1], args[2], args[3], args[4]
        ps_command = (f"Install-WindowsUpdate -MicrosoftUpdate -UpdateID {update_id} "
                      f"-RevisionNumber {revision} -ScheduleJob (Get-Date -Hour {hour} -Minute {minute} -Second 0) "
                      f"-AcceptAll -AutoReboot -Verbose")
        return run_powershell_command(ps_command)
    elif command == "add-microsoft-update-service":
        return run_powershell_command("Add-WUServiceManager -MicrosoftUpdate")
    elif args[0] == "add-offline-sync-service":
        return run_powershell_command(f"Add-WUServiceManager -ScanFileLocation {args[1]}")
    elif command == "get-update-history":
        return run_powershell_command("Get-WUHistory")
    elif command == "get-update-history-24h":
        return run_powershell_command("Get-WUHistory -MaxDate (Get-Date).AddDays(-1)")
    elif args[0] == "uninstall-update":
        return run_powershell_command(f"Get-WUUninstall -KBArticleID {args[1]}")
    elif command == "get-update-settings":
        return run_powershell_command("Get-WUSettings")
    elif args[0] == "set-target-version":
        product_version, target_version = args[1], args[2]
        ps_command = (f"Set-WUSettings -TargetReleaseVersion -TargetReleaseVersionInfo {target_version} "
                      f"-ProductVersion \"{product_version}\"")
        return run_powershell_command(ps_command)
    else:
        return "Unknown command"


def handle_client_connection(conn):
    try:
        while True:
            data = conn.recv(CHUNK_SIZE)
            if not data:
                break
            command = data.decode()
            print(f"Received command: {command}")
            output = handle_client_command(command)

            for i in range(0, len(output), CHUNK_SIZE):
                conn.sendall(output[i:i + CHUNK_SIZE].encode())
            conn.sendall(END_OF_MESSAGE)  # Indicate the end of transmission
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 65432))
        s.listen()
        print("Client is listening for commands...")
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            handle_client_connection(conn)


if __name__ == "__main__":
    main()
