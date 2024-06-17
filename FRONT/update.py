import subprocess

class PowerShellServer:
    def __init__(self):
        pass

    def run_powershell_command(self, command):
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Command failed with error: {result.stderr}"
        return result.stdout

    def set_execution_policy(self):
        return self.run_powershell_command("Set-ExecutionPolicy -ExecutionPolicy Bypass -Force")

    def is_module_installed(self, module_name):
        return module_name in self.run_powershell_command(f"Get-Module -ListAvailable -Name {module_name}")

    def register_psgallery(self):
        return self.run_powershell_command("Register-PSRepository -Default")

    def is_psgallery_registered(self):
        return "PSGallery" in self.run_powershell_command("Get-PSRepository")

    def install_module(self, module_name):
        command = f"Install-Module -Name {module_name} -Force" if module_name == "PSWindowsUpdate" else f"Install-PackageProvider -Name {module_name} -MinimumVersion 2.8.5.201 -Force"
        return self.run_powershell_command(command)

    def import_module(self, module_name):
        return self.run_powershell_command(f"Import-Module -Name {module_name}")

    def ensure_prerequisites(self):
        ps_module = "PSWindowsUpdate"
        nu_module = "NuGet"
        try:
            if not self.is_module_installed(ps_module):
                self.set_execution_policy()
                if not self.is_module_installed(nu_module):
                    self.install_module(nu_module)
                if not self.is_psgallery_registered():
                    self.register_psgallery()
                if not self.is_module_installed("PowerShellGet"):
                    self.install_module("PowerShellGet")
                self.install_module(ps_module)
                self.import_module(ps_module)
        except Exception as e:
            return f"Failed to ensure prerequisites: {e}"
        return "All prerequisites are met."

    def check_and_install_components(self):
        prerequisites = self.ensure_prerequisites()
        if "Failed" in prerequisites:
            return prerequisites

        import_result = self.import_module("PSWindowsUpdate")
        if "Error" in import_result:
            return f"Failed to import PSWindowsUpdate: {import_result}"

        return "PSWindowsUpdate is ready to use."

    def handle_client_command(self, command):
        prerequisite_check = self.check_and_install_components()
        if "Failed" in prerequisite_check:
            return prerequisite_check

        args = command.split()
        if command == "check-updates":
            return self.run_powershell_command("Get-WindowsUpdate")
        elif command == "install-updates":
            return self.run_powershell_command("Install-WindowsUpdate -AcceptAll -AutoReboot")
        elif args[0] == "hide-update":
            return self.run_powershell_command(f"Hide-WindowsUpdate -KBArticleID {args[1]} -Verbose")
        elif args[0] == "schedule-update":
            update_id, revision, hour, minute = args[1], args[2], args[3], args[4]
            ps_command = (f"Install-WindowsUpdate -MicrosoftUpdate -UpdateID {update_id} "
                          f"-RevisionNumber {revision} -ScheduleJob (Get-Date -Hour {hour} -Minute {minute} -Second 0) "
                          f"-AcceptAll -AutoReboot -Verbose")
            return self.run_powershell_command(ps_command)
        elif command == "add-microsoft-update-service":
            return self.run_powershell_command("Add-WUServiceManager -MicrosoftUpdate")
        elif args[0] == "add-offline-sync-service":
            return self.run_powershell_command(f"Add-WUServiceManager -ScanFileLocation {args[1]}")
        elif command == "get-update-history":
            return self.run_powershell_command("Get-WUHistory")
        elif command == "get-update-history-24h":
            return self.run_powershell_command("Get-WUHistory -MaxDate (Get-Date).AddDays(-1)")
        elif args[0] == "uninstall-update":
            return self.run_powershell_command(f"Get-WUUninstall -KBArticleID {args[1]}")
        elif command == "get-update-settings":
            return self.run_powershell_command("Get-WUSettings")
        elif args[0] == "set-target-version":
            product_version, target_version = args[1], args[2]
            ps_command = (f"Set-WUSettings -TargetReleaseVersion -TargetReleaseVersionInfo {target_version} "
                          f"-ProductVersion \"{product_version}\"")
            return self.run_powershell_command(ps_command)
        else:
            return "Unknown command"
