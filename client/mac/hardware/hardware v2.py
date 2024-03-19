import platform
import subprocess
import csv

def get_system_info():
    system_info = {}

    # Get basic system information
    system_info['System'] = platform.system()
    system_info['Node Name'] = platform.node()
    system_info['Release'] = platform.release()
    system_info['Version'] = platform.version()
    system_info['Machine'] = platform.machine()
    system_info['Processor'] = platform.processor()

    # Get CPU information
    try:
        cpu_info = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).strip().decode()
        system_info['CPU'] = cpu_info
    except Exception as e:
        system_info['CPU'] = "N/A"

    # Get memory information
    try:
        memory_info = subprocess.check_output(['sysctl', 'hw.memsize']).strip().decode()
        memory_info = int(memory_info.split()[1]) / (1024 ** 3)  # Convert to GB
        system_info['Memory (GB)'] = memory_info
    except Exception as e:
        system_info['Memory (GB)'] = "N/A"

    # Get serial number
    try:
        serial_number = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode().split("Serial Number (system):")[-1].strip()
        system_info['Serial Number'] = serial_number
    except Exception as e:
        system_info['Serial Number'] = "N/A"

    # Get MAC address and IP address of Wi-Fi interface
    try:
        wifi_info = subprocess.check_output(['ifconfig', 'en0']).decode()
        wifi_mac_address = wifi_info.split('ether ')[1].split(' ')[0]
        system_info['Wi-Fi MAC Address'] = wifi_mac_address
        wifi_ip_address = wifi_info.split('inet ')[1].split(' ')[0]
        system_info['Wi-Fi IP Address'] = wifi_ip_address
    except Exception as e:
        system_info['Wi-Fi MAC Address'] = "N/A"
        system_info['Wi-Fi IP Address'] = "N/A"

    # Get MAC address and IP address of Ethernet interface if exists
    try:
        ethernet_info = subprocess.check_output(['ifconfig', 'en1']).decode()
        ethernet_mac_address = ethernet_info.split('ether ')[1].split(' ')[0]
        system_info['Ethernet MAC Address'] = ethernet_mac_address
        ethernet_ip_address = ethernet_info.split('inet ')[1].split(' ')[0]
        system_info['Ethernet IP Address'] = ethernet_ip_address
    except Exception as e:
        system_info['Ethernet MAC Address'] = "N/A"
        system_info['Ethernet IP Address'] = "N/A"

    # Get storage information
    try:
        storage_info = subprocess.check_output(['diskutil', 'list']).decode()
        disks = [line.split()[0] for line in storage_info.splitlines() if line.strip().startswith('/dev')]
        for disk in disks:
            disk_info = subprocess.check_output(['diskutil', 'info', disk]).decode()
            disk_type = 'Internal' if 'Internal:' in disk_info else 'Physical'
            disk_name = [line.split(':')[-1].strip() for line in disk_info.splitlines() if 'Device / Media Name:' in line][0]
            storage_type = 'HDD' if 'Container' in disk_name else 'SSD' if 'SSD' in disk_name else 'Unknown'
            system_info[f'{disk_type} Disk Type'] = storage_type
            system_info[f'{disk_type} Disk Name'] = disk_name
    except Exception as e:
        system_info['Internal Disk Type'] = "N/A"
        system_info['Internal Disk Name'] = "N/A"
        system_info['Physical Disk Type'] = "N/A"
        system_info['Physical Disk Name'] = "N/A"

    return system_info

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=':', lineterminator='\n')
        writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    system_info = get_system_info()
    print("System Information:")
    for key, value in system_info.items():
        print(f"{key}: {value}")

    # Save to CSV
    save_to_csv(system_info, 'system_info.csv')
    print("System information saved to 'system_info.csv'")
