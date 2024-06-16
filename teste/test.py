import datetime
import platform
import psutil
import shutil
import sys
import socket
from pySMART import *
import clr  # the pythonnet module

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware
import wmi


def send_data(label, data):
    print(f"Sending {label}: {data}")


def power():
    sensor_data = []
    cpu_name = ""
    igpu_names = set()
    dgpu_names = set()

    computer = Hardware.Computer()
    computer.IsCpuEnabled = True
    computer.IsGpuEnabled = True
    computer.Open()

    total_cpu_power = 0.0
    total_igpu_power = 0.0
    total_dgpu_power = 0.0

    try:
        for hardware in computer.Hardware:
            if hardware.HardwareType in (Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia,
                                         Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
                hardware.Update()
                device_name = hardware.Name  # Get the name of the device
                if hardware.HardwareType == Hardware.HardwareType.Cpu:
                    cpu_name = device_name
                elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
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

                for sensor in hardware.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Power and sensor.Value is not None:
                        value = sensor.Value
                        if hardware.HardwareType == Hardware.HardwareType.Cpu:
                            total_cpu_power += value
                        elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd,
                                                       Hardware.HardwareType.GpuNvidia):
                            if any(keyword in hardware.Name for keyword in
                                   ["Vega", "Radeon Graphics", "UHD Graphics", "Iris Xe Graphics"]):
                                total_igpu_power += value
                            else:
                                total_dgpu_power += value
    except Exception as e:
        print(f"Error collecting sensor data: {e}")
    finally:
        computer.Close()

    power_data = {
        "cpu_name": cpu_name,
        "gpu_names": list(dgpu_names),
        "igpu_names": list(igpu_names),
        "cpu_power": total_cpu_power,
        "igpu_power": total_igpu_power,
        "dgpu_power": total_dgpu_power
    }

    send_data("power", power_data)
    return power_data


def system_info():
    system_info = {
        "time": datetime.datetime.now().strftime("%I:%M:%S %p"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "machine": platform.machine(),
        "version": platform.version(),
        "platform": platform.platform(),
        "system": platform.system(),
        "processor": platform.processor(),
        "hostname": socket.gethostname()
    }

    send_data("system_info", system_info)
    return system_info


def storage_info():
    storage_data = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = shutil.disk_usage(part.mountpoint)
            smart_device = Smart(part.device)
            device_name = smart_device.serial if smart_device.serial else "Unknown"
        except Exception:
            device_name = "Unknown"

        storage_info = {
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "opts": part.opts,
            "total_space": f"{usage.total / (1024 ** 3):.2f} GB",
            "free_space": f"{usage.free / (1024 ** 3):.2f} GB",
            "used_space": f"{usage.used / (1024 ** 3):.2f} GB",
            "device_name": device_name
        }
        storage_data.append(storage_info)

    send_data("storage_info", storage_data)
    return storage_data


def ram_info():
    ram_data = []
    total_ram = 0
    if sys.platform == 'win32':
        w = wmi.WMI()
        for mem in w.Win32_PhysicalMemory():
            total_ram += int(mem.Capacity)
            form_factor = {8: "DIMM", 12: "SODIMM"}.get(mem.FormFactor, "Unknown")

            ram_data.append({
                'capacity': f"{int(mem.Capacity) / (1024 ** 3):.2f} GB",
                'speed': mem.Speed,
                'manufacturer': mem.Manufacturer,
                'part_number': mem.PartNumber,
                'serial_number': mem.SerialNumber,
                'form_factor': form_factor
            })
    else:
        # Implement for other platforms if needed
        pass

    send_data("ram_info", ram_data)
    return ram_data


def network_data():
    if_stats_data = []

    for interface, stats in psutil.net_if_stats().items():
        if_addrs = psutil.net_if_addrs().get(interface, [])
        mac_address = None
        ip_address = None
        for addr in if_addrs:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
            elif addr.family == socket.AF_INET:
                ip_address = addr.address

        if_stats_data.append({
            'interface': interface,
            'is_up': stats.isup,
            'duplex': stats.duplex,
            'speed': stats.speed,
            'mtu': stats.mtu,
            'mac_address': mac_address,
            'ip_address': ip_address
        })

    send_data("network_data", if_stats_data)
    return if_stats_data


def combined_info():
    power_data = power()
    system_data = system_info()
    storage_data = storage_info()
    ram_data = ram_info()
    network = network_data()

    combined_data = {
        "cpu_name": power_data.get("cpu_name"),
        "gpu_names": power_data.get("gpu_names"),
        "igpu_names": power_data.get("igpu_names"),
        "os_name": system_data.get("system"),
        "os_version": system_data.get("version"),
        "hostname": system_data.get("hostname"),
        "storage_devices": storage_data,
        "ram_info": ram_data,
        "network_data": network
    }

    send_data("combined_info", combined_data)

    # Print the combined data
    print("Combined Information:")
    for key, value in combined_data.items():
        print(f"{key}: {value}")

    # Print each GPU and iGPU name
    print("\nList of GPUs:")
    for gpu_name in power_data.get("gpu_names"):
        print(f"GPU: {gpu_name}")

    print("\nList of iGPUs:")
    for igpu_name in power_data.get("igpu_names"):
        print(f"iGPU: {igpu_name}")

    return combined_data


# Example call to the combined_info function
combined_info()