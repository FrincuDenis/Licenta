import psutil
import clr  # the pythonnet module
import threading
import time

clr.AddReference(r'OpenHardwareMonitorLib')
# e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll

from OpenHardwareMonitor.Hardware import Computer

# Initialize Computer object
c = Computer()
c.CPUEnabled = True  # get the Info about CPU
c.GPUEnabled = True  # get the Info about GPU
c.Open()

def monitor_cpu():
    while True:
        for a in range(0, len(c.Hardware[0].Sensors)):
            if "/amdcpu/0/power/0" in str(c.Hardware[0].Sensors[a].Identifier):
                value = c.Hardware[0].Sensors[a].get_Value()
                if value is not None:
                    formatted_value = "{:.2f}".format(value)
                    print(f"Cpu: {formatted_value}")
                c.Hardware[0].Update()
                time.sleep(3)  # Sleep to avoid busy-waiting

def monitor_gpu():
    while True:
        for a in range(0, len(c.Hardware[1].Sensors)):
            if "/atigpu/0/power/0" in str(c.Hardware[1].Sensors[a].Identifier):
                value = c.Hardware[1].Sensors[a].get_Value()
                if value is not None:
                    formatted_value = "{:.2f}".format(value)
                    print(f"Gpu: {formatted_value}")
                c.Hardware[1].Update()
                time.sleep(3)  # Sleep to avoid busy-waiting

def get_cpu_usage():
    """Returns the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    """Returns the current RAM usage."""
    ram_info = psutil.virtual_memory()
    return {
        'total': ram_info.total,
        'available': ram_info.available,
        'used': ram_info.used,
        'percent': ram_info.percent
    }


def get_disk_usage():
    """Returns the current disk usage for each partition."""
    partitions = psutil.disk_partitions()
    usage_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        usage_info.append({
            'device': partition.device,
            'fstype': partition.fstype,
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        })
    return usage_info


def main():
    print("CPU Usage: {}%".format(get_cpu_usage()))

    ram_usage = get_ram_usage()
    print("\nRAM Usage:")
    print("Total: {:.2f} GB".format(ram_usage['total'] / (1024 ** 3)))
    print("Available: {:.2f} GB".format(ram_usage['available'] / (1024 ** 3)))
    print("Used: {:.2f} GB".format(ram_usage['used'] / (1024 ** 3)))
    print("Percent: {}%".format(ram_usage['percent']))

    print("\nDisk Usage:")
    for partition in get_disk_usage():
        print("Device: {}".format(partition['device']))
        print("File system type: {}".format(partition['fstype']))
        print("Total: {:.2f} GB".format(partition['total'] / (1024 ** 3)))
        print("Used: {:.2f} GB".format(partition['used'] / (1024 ** 3)))
        print("Free: {:.2f} GB".format(partition['free'] / (1024 ** 3)))
        print("Percent: {}%".format(partition['percent']))
        print("")


if __name__ == "__main__":
    main()
