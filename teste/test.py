
'''
import wmi

def get_ram_information():
    try:
        c = wmi.WMI()
        physical_memory = c.Win32_PhysicalMemory()
        ram_info = {}
        for stick in physical_memory:
            capacity_gb = int(stick.Capacity) / (1024 ** 3)  # Convert bytes to gigabytes
            manufacturer = stick.Manufacturer
            if manufacturer not in ram_info:
                ram_info[manufacturer] = {"Count": 1, "TotalCapacity": capacity_gb, "CapacityList": set([capacity_gb])}
            else:
                ram_info[manufacturer]["Count"] += 1
                ram_info[manufacturer]["TotalCapacity"] += capacity_gb
                ram_info[manufacturer]["CapacityList"].add(capacity_gb)
        return ram_info
    except Exception as e:
        print(f"Error retrieving RAM information: {e}")
        return None

# Example usage:
ram_info = get_ram_information()
if ram_info is not None:
    for manufacturer, info in ram_info.items():
        sticks = 'x'.join([str(capacity) + 'GB' for capacity in sorted(info["CapacityList"])])
    print(f"{manufacturer} - sticks {info['Count']} X {sticks},total capacity: {round(info['TotalCapacity'], 2)} GB ")









    # Constructing the output string
output = f"""
PCName              = {computer_name}
MAC_AddressEthernet = {mac_addresses.get('Ethernet', 'N/A')}
IPAddressEthernet   = {ip_addresses.get('Ethernet', 'N/A')}
MAC_AddressWifi     = {mac_addresses.get('Wi-Fi', 'N/A')}
IPAddressWifi       = {ip_addresses.get('Wi-Fi', 'N/A')}
Drive               = {drive_models}
DriveSizeGB         = {total_drive_size_gb:.2f}
UsedDriveSpaceGB    = {used_drive_space_gb:.2f}
RAM                 = {ram}
CPUModel            = {cpu_model}
OS                  = {os_system} {os_release}
"""

print(output)

'''
import subprocess

import wmi

def get_computer_name():
    try:
        c = wmi.WMI()
        for computer in c.Win32_ComputerSystem():
            return computer.Name
    except Exception as e:
        print(f"Error retrieving computer name: {e}")
        return "Unknown"

def get_mac_addresses():
    try:
        c = wmi.WMI()
        interfaces = c.Win32_NetworkAdapter()
        mac_addresses = {}
        for interface in interfaces:
            if interface.MACAddress is not None:
                mac_addresses[interface.Name] = interface.MACAddress
        return mac_addresses
    except Exception as e:
        print(f"Error retrieving MAC addresses: {e}")
        return {}

def get_ip_addresses():
    try:
        c = wmi.WMI()
        interfaces = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        ip_addresses = {}
        for interface in interfaces:
            ip_addresses[interface.Description] = interface.IPAddress[0]
        return ip_addresses
    except Exception as e:
        print(f"Error retrieving IP addresses: {e}")
        return {}

def get_drive_model():
    c = wmi.WMI()
    disks = c.Win32_DiskDrive()
    partitions = []
    for disk in disks:
        # Get model information
        model = disk.Model
        partitions.append(model)
        # Get partitions information


    return partitions
def get_drive_information():
    try:
        c = wmi.WMI()

        drives = c.Win32_LogicalDisk()
        drive_info = []
        drive_model = get_drive_model()
        for drive in drives:
            drive_info.append({
                "Drive": drive.Caption,
                "Model": drive_model[0],
                "TotalSizeGB": int(drive.Size) / (1024 ** 3),
                "UsedSpaceGB": (int(drive.Size) - int(drive.FreeSpace)) / (1024 ** 3)
            })
            drive_model.pop(0)
        return drive_info
    except Exception as e:
        print(f"Error retrieving drive information: {e}")
        return []


def get_ram_information():
    try:
        c = wmi.WMI()
        physical_memory = c.Win32_PhysicalMemory()
        ram_info = {}
        for stick in physical_memory:
            capacity_gb = int(stick.Capacity) / (1024 ** 3)  # Convert bytes to gigabytes
            manufacturer = stick.Manufacturer
            if manufacturer not in ram_info:
                ram_info[manufacturer] = {"Count": 1, "TotalCapacity": capacity_gb, "CapacityList": set([capacity_gb])}
            else:
                ram_info[manufacturer]["Count"] += 1
                ram_info[manufacturer]["TotalCapacity"] += capacity_gb
                ram_info[manufacturer]["CapacityList"].add(capacity_gb)
        return ram_info
    except Exception as e:
        print(f"Error retrieving RAM information: {e}")
        return {}

def get_cpu_information():
    try:
        c = wmi.WMI()
        processors = c.Win32_Processor()
        cpu_info = []
        for processor in processors:
            cpu_info.append({
                "Name": processor.Name.strip(),
                "Manufacturer": processor.Manufacturer.strip(),
                "MaxClockSpeed": processor.MaxClockSpeed,
                "NumberOfCores": processor.NumberOfCores
            })
        return cpu_info
    except Exception as e:
        print(f"Error retrieving CPU information: {e}")
        return []

def get_gpu_information():
    try:
        c = wmi.WMI()
        gpus = c.Win32_VideoController()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "Name": gpu.Caption.strip(),
                "DriverVersion": gpu.DriverVersion,
                "AdapterRAM": int(gpu.AdapterRAM) / (1024 ** 3)  # Convert bytes to gigabytes
            })
        return gpu_info
    except Exception as e:
        print(f"Error retrieving GPU information: {e}")
        return []
def get_os_information():
    try:
        c = wmi.WMI()
        os_info = c.Win32_OperatingSystem()[0]
        return {
            "Name": os_info.Caption.strip(),
            "Version": os_info.Version,
            "Architecture": os_info.OSArchitecture,
            "InstallDate": os_info.InstallDate.split('.')[0]  # Remove milliseconds from InstallDate
        }
    except Exception as e:
        print(f"Error retrieving OS information: {e}")
        return {}

# Get OS information


# Print OS information


# Get hardware information
computer_name = get_computer_name()
mac_addresses = get_mac_addresses()
ip_addresses = get_ip_addresses()
drive_info = get_drive_information()
ram_info = get_ram_information()
cpu_info = get_cpu_information()
gpu_info = get_gpu_information()
os_info = get_os_information()
# Print hardware information
print(f"Computer Name: {computer_name}")
print("MAC Addresses:")
for interface, mac_address in mac_addresses.items():
    print(f"  {interface}: {mac_address}")
print("IP Addresses:")
for interface, ip_address in ip_addresses.items():
    print(f"  {interface}: {ip_address}")

print("\nDrive Information:")
for drive in drive_info:
    print(f"  Drive: {drive['Drive']}")
    print(f"    Model: {drive['Model']}")
    print(f"    Total Size: {drive['TotalSizeGB']:.2f} GB")
    print(f"    Used Space: {drive['UsedSpaceGB']:.2f} GB")

print("\nRAM Information:")
for manufacturer, info in ram_info.items():
    sticks = 'x'.join([str(capacity) + 'GB' for capacity in sorted(info["CapacityList"])])
    print(f"  {manufacturer} - sticks {info['Count']} X {sticks}, total capacity: {round(info['TotalCapacity'], 2)} GB")

print("\nCPU Information:")
for cpu in cpu_info:
    print(f"  Name: {cpu['Name']}")
    print(f"  Manufacturer: {cpu['Manufacturer']}")
    print(f"  Max Clock Speed: {cpu['MaxClockSpeed']} MHz")
    print(f"  Number of Cores: {cpu['NumberOfCores']}")
    print("\nGPU Information:")
for gpu in gpu_info:
        print(f"  Name: {gpu['Name']}")
        print(f"  Driver Version: {gpu['DriverVersion']}")
        print(f"  Adapter RAM: {gpu['AdapterRAM']:.2f} GB")
        print()
print("\nOS Information:")
print(f"  Name: {os_info['Name']}")
print(f"  Version: {os_info['Version']}")
print(f"  Architecture: {os_info['Architecture']}")
print(f"  Install Date: {os_info['InstallDate']}")




