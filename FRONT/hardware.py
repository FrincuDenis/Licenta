import subprocess
import json
import platform
import sys
import clr  # the pythonnet module

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware
import wmi


class HardwareInfoCollector:
    def __init__(self):
        self.hardware_data = {}
        self.ram_data = []

    def run_powershell_command(self, command):
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return None
            return result.stdout.strip()
        except Exception as e:
            print(f"Failed to run PowerShell command: {e}")
            return None

    def set_execution_policy(self, policy):
        return self.run_powershell_command(f"Set-ExecutionPolicy {policy} -Scope CurrentUser -Force")

    def get_execution_policy(self):
        return self.run_powershell_command("Get-ExecutionPolicy -Scope CurrentUser")

    def run_powershell_script(self, script_path):
        try:
            result = subprocess.run(["powershell", "-File", script_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return None
            return result.stdout
        except Exception as e:
            print(f"Failed to run PowerShell script: {e}")
            return None

    def get_hardware_name(self):
        igpu_names = set()
        dgpu_names = set()

        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.Open()

        try:
            for hardware in computer.Hardware:
                if hardware.HardwareType in (Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia,
                                             Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
                    hardware.Update()
                    device_name = hardware.Name  # Get the name of the device
                    if hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                        if any(keyword in device_name for keyword in
                               ["Integrated", "iGPU", "Intel Iris", "UHD Graphics"]):
                            igpu_names.add(device_name)
                        else:
                            dgpu_names.add(device_name)
                    elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
                        if any(keyword in device_name for keyword in ["APU", "Radeon Vega", "Radeon Graphics"]):
                            igpu_names.add(device_name)
                        else:
                            dgpu_names.add(device_name)
                    elif hardware.HardwareType == Hardware.HardwareType.GpuNvidia:
                        dgpu_names.add(device_name)
        except Exception as e:
            print(f"Error collecting sensor data: {e}")
        finally:
            computer.Close()

        self.hardware_data = {
            "gpu_names": list(dgpu_names),
            "igpu_names": list(igpu_names)
        }

        self.send_data("hardware", self.hardware_data)

    def collect_ram_info(self):
        if sys.platform == 'win32':
            w = wmi.WMI()
            for mem in w.Win32_PhysicalMemory():
                self.ram_data.append({
                    'manufacturer': mem.Manufacturer,
                    'part_number': mem.PartNumber,
                })
        else:
            # Implement for other platforms if needed
            pass

        self.send_data("ram_info", self.ram_data)

    def send_data(self, label, data):
        print(f"Sending {label}: {data}")

    def parse_and_print_info(self, powershell_output):
        try:
            data = json.loads(powershell_output)

            # Extract dgpu_names and igpu_names from hardware_data
            dgpu_names = self.hardware_data.get("gpu_names", [])
            igpu_names = self.hardware_data.get("igpu_names", [])

            # Join the GPU names with semicolons if there are multiple
            dgpu_names_str = "; ".join(dgpu_names)
            igpu_names_str = "; ".join(igpu_names)

            # Join the RAM details
            ram_manufacturers = "; ".join(ram['manufacturer'] for ram in self.ram_data)
            ram_part_numbers = "; ".join(ram['part_number'] for ram in self.ram_data)

            # Construct new ordered data with dgpu_names, igpu_names, manufacturer, and part_number
            ordered_data = {}
            for key, value in data.items():
                ordered_data[key] = value
                if key == "UsedDriveSpaceGB":
                    ordered_data["RAM_Manufacturer"] = ram_manufacturers
                    ordered_data["RAM_PartNumber"] = ram_part_numbers
                if key == "CPUModel":
                    ordered_data["dgpu_names"] = dgpu_names_str
                    ordered_data["igpu_names"] = igpu_names_str
                elif key == "OS":
                    break

            # Get OS version using platform module
            os_version = platform.version()
            ordered_data["OSVersion"] = os_version

            # Wrap everything in a hardware dictionary

            return ordered_data


        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")

    def collect_all_info(self, script_path):
        # Save the current execution policy
        original_policy = self.get_execution_policy()
        print(f"Original Execution Policy: {original_policy}")

        # Set the execution policy to RemoteSigned or Unrestricted
        self.set_execution_policy("RemoteSigned")

        # Run the PowerShell script
        powershell_output = self.run_powershell_script(script_path)

        # Collect power info (GPU and CPU power consumption)
        self.get_hardware_name()

        # Collect RAM info
        self.collect_ram_info()

        if powershell_output:
           return self.parse_and_print_info(powershell_output)

        # Revert the execution policy back to the original state
        if original_policy:
            self.set_execution_policy(original_policy)
            return (f"Execution Policy reverted to: {original_policy}")


if __name__ == "__main__":
    script_path = "system_info.ps1"
    collector = HardwareInfoCollector()
    collector.collect_all_info(script_path)
