import argparse
import subprocess


def run_powershell_command(command):
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr}")
    return result.stdout


def set_execution_policy():
    command = "Set-ExecutionPolicy -ExecutionPolicy Bypass -Force"
    return run_powershell_command(command)


def is_module_installed(module_name):
    command = f"Get-Module -ListAvailable -Name {module_name}"
    result = run_powershell_command(command)
    return module_name in result


def register_psgallery():
    command = "Register-PSRepository -Default"
    return run_powershell_command(command)


def is_psgallery_registered():
    command = "Get-PSRepository"
    result = run_powershell_command(command)
    return "PSGallery" in result


def install_module(module_name):
    if(module_name == "PSWindowsUpdate"):
        command = f"Install-Module -Name {module_name} -Force "
    else:
        command = f"Install-PackageProvider -Name {module_name} -MinimumVersion 2.8.5.201 -Force"
    return run_powershell_command(command)


def import_module(module_name):
    command = f"Import-Module -Name {module_name}"
    return run_powershell_command(command)


def check_for_updates():
    command = "Get-WindowsUpdate"
    return run_powershell_command(command)


def install_updates():
    command = "Install-WindowsUpdate -AcceptAll -AutoReboot"
    return run_powershell_command(command)


def hide_update(kb_article_id):
    command = f"Hide-WindowsUpdate -KBArticleID {kb_article_id} -Verbose"
    return run_powershell_command(command)


def schedule_update_install(update_id, revision_number, hour, minute):
    command = (f"Install-WindowsUpdate -MicrosoftUpdate -UpdateID {update_id} "
               f"-RevisionNumber {revision_number} -ScheduleJob (Get-Date -Hour {hour} -Minute {minute} -Second 0) "
               f"-AcceptAll -AutoReboot -Verbose")
    return run_powershell_command(command)


def add_microsoft_update_service():
    command = "Add-WUServiceManager -MicrosoftUpdate"
    return run_powershell_command(command)


def add_offline_sync_service(file_path):
    command = f"Add-WUServiceManager -ScanFileLocation {file_path}"
    return run_powershell_command(command)


def get_update_history():
    command = "Get-WUHistory"
    return run_powershell_command(command)


def get_update_history_last_24h():
    command = "Get-WUHistory -MaxDate (Get-Date).AddDays(-1)"
    return run_powershell_command(command)


def uninstall_update(kb_article_id):
    command = f"Get-WUUninstall -KBArticleID {kb_article_id}"
    return run_powershell_command(command)


def get_update_settings():
    command = "Get-WUSettings"
    return run_powershell_command(command)


def set_target_release_version(product_version, target_release_version):
    command = (f"Set-WUSettings -TargetReleaseVersion -TargetReleaseVersionInfo {target_release_version} "
               f"-ProductVersion \"{product_version}\"")
    return run_powershell_command(command)


def install_powershellget():
    command = "Install-Module -Name PowerShellGet -Force -Confirm:$false"
    return run_powershell_command(command)


def main():
    parser = argparse.ArgumentParser(description="Perform various Windows Update tasks using PowerShell.")
    parser.add_argument("--check-updates", action="store_true", help="Check for Windows updates.")
    parser.add_argument("--install-updates", action="store_true", help="Install available Windows updates.")
    parser.add_argument("--hide-update", metavar="KBID", help="Hide a specific update by KBArticleID.")
    parser.add_argument("--schedule-update", nargs=4, metavar=("UPDATE_ID", "REVISION", "HOUR", "MINUTE"),
                        help="Schedule an update installation.")
    parser.add_argument("--add-microsoft-update-service", action="store_true",
                        help="Register Microsoft Update service as Service Manager.")
    parser.add_argument("--add-offline-sync-service", metavar="FILE_PATH",
                        help="Register Offline Sync Service from a file.")
    parser.add_argument("--get-update-history", action="store_true", help="Get Windows Update history.")
    parser.add_argument("--get-update-history-24h", action="store_true",
                        help="Get Windows Update history for the last 24 hours.")
    parser.add_argument("--uninstall-update", metavar="KBID", help="Uninstall a specific update by KBArticleID.")
    parser.add_argument("--get-update-settings", action="store_true",
                        help="Get current Windows Update Client configuration.")
    parser.add_argument("--set-target-version", nargs=2, metavar=("PRODUCT_VERSION", "TARGET_VERSION"),
                        help="Set the target version for feature updates.")

    args = parser.parse_args()

    ps = "PSWindowsUpdate"
    nu = "NuGet"
    try:
        if not is_module_installed(ps):
            print("Setting execution policy...")
            set_execution_policy()
            print("Execution policy set successfully.")
            if not is_module_installed(nu):
                print(f"Module {nu} is not installed. Installing now...")
                install_module(nu)
                print(f"Module {nu} installed successfully.")
            else:
                print(f"Module {nu} is already installed.")

            # Check if PSGallery is registered
            if not is_psgallery_registered():
                print("PSGallery is not registered. Registering now...")
                register_psgallery()
                print("PSGallery registered successfully.")
            else:
                print("PSGallery is already registered.")

            # Check if PowerShellGet module is installed
            if not is_module_installed("PowerShellGet"):
                print("PowerShellGet module is not installed. Installing now...")
                install_powershellget()
                print("PowerShellGet module installed successfully.")
            else:
                print("PowerShellGet module is already installed.")
            print(f"Module {ps} is not installed. Installing now...")
            install_module(ps)
            print(f"Module {ps} installed successfully.")
            # Import the PSWindowsUpdate module
            print(f"Importing module {ps}...")
            import_module(ps)
            print(f"Module {ps} imported successfully.")
        else:
            print(f"Module {ps} is already installed.")
            # Perform the requested actions
            if args.check_updates:
                print("Checking for updates...")
                updates = check_for_updates()
                print(updates)

            if args.install_updates:
                print("Installing updates...")
                install_result = install_updates()
                print(install_result)

            if args.hide_update:
                print(f"Hiding update with KBArticleID: {args.hide_update}")
                hide_update_result = hide_update(args.hide_update)
                print(hide_update_result)

            if args.schedule_update:
                update_id, revision, hour, minute = args.schedule_update
                print(f"Scheduling update installation at {hour}:{minute}...")
                schedule_result = schedule_update_install(update_id, revision, hour, minute)
                print(schedule_result)

            if args.add_microsoft_update_service:
                print("Registering Microsoft Update service as Service Manager...")
                add_microsoft_update_service_result = add_microsoft_update_service()
                print(add_microsoft_update_service_result)

            if args.add_offline_sync_service:
                file_path = args.add_offline_sync_service
                print(f"Registering Offline Sync Service from file {file_path}...")
                add_offline_sync_service_result = add_offline_sync_service(file_path)
                print(add_offline_sync_service_result)

            if args.get_update_history:
                print("Getting Windows Update history...")
                update_history = get_update_history()
                print(update_history)

            if args.get_update_history_24h:
                print("Getting Windows Update history for the last 24 hours...")
                update_history_last_24h = get_update_history_last_24h()
                print(update_history_last_24h)

            if args.uninstall_update:
                print(f"Uninstalling update with KBArticleID: {args.uninstall_update}")
                uninstall_update_result = uninstall_update(args.uninstall_update)
                print(uninstall_update_result)

            if args.get_update_settings:
                print("Getting current Windows Update Client configuration...")
                update_settings = get_update_settings()
                print(update_settings)

            if args.set_target_version:
                product_version, target_version = args.set_target_version
                print(f"Setting the target version for feature updates to {product_version} {target_version}...")
                set_target_version_result = set_target_release_version(product_version, target_version)
                print(set_target_version_result)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
