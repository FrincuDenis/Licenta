import shutil
import socket
import sys
import json
import threading

import psutil
import time
import platform
import datetime
import psutil
import clr  # the pythonnet module
from time import sleep
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware
platforms={
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'Mac x',
    'win32': 'Windows',
}
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chunk_size = 7168
    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
    def send_data(self, process_data,name):
        if name == '0':
            json_data = json.dumps(process_data)
        else:
            json_data = json.dumps({name: process_data})
        for i in range(0, len(json_data), self.chunk_size):
            chunk = json_data[i:i + self.chunk_size]
            self.client_socket.sendall(chunk.encode())
            time.sleep(0.1)
        self.client_socket.sendall(b'\0')
    def cpu_ram(self):
            total_ram = 1.0
            total_ram = psutil.virtual_memory()[0] * total_ram
            total_ram = total_ram / (1024 * 1024 * 1024)

            available_ram = 1.0
            available_ram = psutil.virtual_memory()[1] * available_ram
            available_ram = available_ram / (1024 * 1024 * 1024)

            ram_usage = psutil.virtual_memory().percent

            used_ram = 1.0
            used_ram = psutil.virtual_memory()[3] * used_ram
            used_ram = used_ram / (1024 * 1024 * 1024)

            ram_free = 1.0
            ram_free = psutil.virtual_memory()[4] * ram_free
            ram_free = ram_free / (1024 * 1024 * 1024)

            core = psutil.cpu_count()
            cpu_per = psutil.cpu_percent()
            cpu_main_core = psutil.cpu_count(logical=False)

            # Prepare CPU percentage data to send to the server
            cpu_data = {
                "core_count": core,
                "cpu_percentage": cpu_per,
                "main_core_count": cpu_main_core,
                "total_ram": total_ram,
                "available_ram": available_ram,
                "ram_usage": ram_usage,
                "used_ram": used_ram,
                "ram_free": ram_free,
            }

            # Send CPU percentage data to the server
            self.send_data(cpu_data,'0')

    def power(self):
            computer = Hardware.Computer()
            computer.IsCpuEnabled = True
            computer.IsGpuEnabled = True
            computer.Open()

            total_cpu_power = 0.0
            total_igpu_power = 0.0
            total_dgpu_power = 0.0

            for hardware in computer.Hardware:
                if hardware.HardwareType in (
                        Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd,
                        Hardware.HardwareType.GpuIntel):
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Power:
                            value = sensor.Value
                            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                                if value is not None:
                                    total_cpu_power += value
                            elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                                if "UHD" in hardware.Name or "Iris" in hardware.Name:
                                    total_igpu_power += value
                                else:
                                    total_dgpu_power += value
                            elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
                                if "Vega" in hardware.Name or "Radeon Graphics" in hardware.Name:
                                    total_igpu_power += value
                                else:
                                    total_dgpu_power += value
                            elif hardware.HardwareType == Hardware.HardwareType.GpuNvidia:
                                total_dgpu_power += value

            computer.Close()

            power_data = {
                "cpu_power": total_cpu_power,
                "igpu_power": total_igpu_power,
                "dgpu_power": total_dgpu_power
            }
            # Send power consumption data to the server
            self.send_data(power_data,'0')

    def battery(self):
            battery = psutil.sensors_battery()
            battery_info = {}
            if battery is not None:
                battery_info["charge"] = round(battery.percent, 2)
                if battery.power_plugged:
                    battery_info["status"] = "Charging" if battery.percent < 100 else "Fully Charged"
                    battery_info["time_left"] = "N/A"
                else:
                    battery_info["status"] = "Discharging" if battery.percent < 100 else "Fully Charged"
                    battery_info["time_left"] = self.secs2hours(battery.secsleft)
                battery_info["plugged"] = "Yes" if battery.power_plugged else "No"
            else:
                battery_info["status"] = "Platform not supported"
                battery_info["charge"] = 100
                battery_info["plugged"] = "No"
                battery_info["time_left"] = "N/A"

            # Send battery information to the server
            self.send_data(battery_info, '0')
    def secs2hours(self, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d (H:M:S)" % (hh, mm, ss)

    def system_info(self):
        system_info = {
            "time": datetime.datetime.now().strftime("%I:%M:%S %p"),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "machine": platform.machine(),
            "version": platform.version(),
            "platform": platform.platform(),
            "system": platform.system(),
            "processor": platform.processor()
        }

        # Send system information to the server
        self.send_data(system_info, '0')

    def processes(self):
        process_data = []

        current_pids = set(psutil.pids())
        for pid in current_pids:
            try:
                process = psutil.Process(pid)
                process_info = {
                    "pid": str(process.pid),
                    "name": process.name(),
                    "status": process.status(),
                    "create_time": datetime.datetime.utcfromtimestamp(process.create_time()).strftime(
                        '%Y-%m-%d %H:%M:%S')
                }
                process_data.append(process_info)
            except Exception as e:
                print(e)

        self.send_data(process_data,'0')

    def storage_info(self):
        storage_data = []

        storage_device = psutil.disk_partitions(all=False)
        for x in storage_device:
            disk_usage = shutil.disk_usage(x.mountpoint)
            storage_info = {
                "device": x.device,
                "mountpoint": x.mountpoint,
                "fstype": x.fstype,
                "opts": x.opts,
                "total_space": f"{disk_usage.total / (1024 ** 3):.2f} GB",
                "free_space": f"{disk_usage.free / (1024 ** 3):.2f} GB",
                "used_space": f"{disk_usage.used / (1024 ** 3):.2f} GB"
            }
            if sys.platform.startswith('linux'):
                storage_info["maxfile"] = str(x.maxfile)
                storage_info["maxpath"] = str(x.maxpath)
            else:
                platform_msg = f"Function not available on {platforms.get(sys.platform, 'this platform')}"
                storage_info["maxfile"] = platform_msg
                storage_info["maxpath"] = platform_msg
            storage_data.append(storage_info)

        self.send_data(storage_data,'0')
    def sensor_data(self):
        sensor_data = []
        cpu_temps = {}
        gpu_temps = {}
        try:
            computer = Hardware.Computer()
            computer.IsCpuEnabled = True
            computer.IsGpuEnabled = True
            computer.Open()

            for hardware in computer.Hardware:
                if hardware.HardwareType in (Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia,
                                             Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Temperature and sensor.Value is not None:
                            temp_value = sensor.Value
                            sensor_name = sensor.Name
                            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                                    cpu_temps.setdefault(sensor_name, []).append(temp_value)
                            elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd,
                                                           Hardware.HardwareType.GpuNvidia):
                                    gpu_temps.setdefault(sensor_name, []).append(temp_value)

            # Append sensor data for each sensor to the list
            for sensor_name, temp_value in cpu_temps.items():
                sensor_data.append({"sensor_type": "CPU", "sensor_name": sensor_name, "value": temp_value})
            for sensor_name, temp_value in gpu_temps.items():
                sensor_data.append({"sensor_type": "GPU", "sensor_name": sensor_name, "value": temp_value})

        except Exception as e:
            print(f"Error initializing hardware monitor: {e}")
        finally:
            computer.Close()

        # Serialize sensor data to JSON
        self.send_data(sensor_data,'0')
    def network_data(self):
        # Send network interface stats
        if_stats_data = []
        for interface, stats in psutil.net_if_stats().items():
            if_stats_data.append({
                'interface': interface,
                'is_up': stats.isup,
                'duplex': stats.duplex,
                'speed': stats.speed,
                'mtu': stats.mtu
            })
        self.send_data(if_stats_data,'0')
        # Send network connections
    def io(self):
        io_counters_data = {}
        for interface, counters in psutil.net_io_counters(pernic=True).items():
            io_counters_data[interface] = {
                'bytes_sent': counters.bytes_sent,
                'bytes_recv': counters.bytes_recv,
                'packets_sent': counters.packets_sent,
                'packets_recv': counters.packets_recv,
                'errin': counters.errin,
                'errout': counters.errout,
                'dropin': counters.dropin,
                'dropout': counters.dropout
            }
        self.send_data(io_counters_data, '0')

    def if_addr(self):
        if_addrs_data = {}
        for interface, addrs in psutil.net_if_addrs().items():
            if_addrs_data[interface] = []
            for addr in addrs:
                if_addrs_data[interface].append({
                    'family': addr.family,
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast,
                    'ptp': addr.ptp
                })
        self.send_data(if_addrs_data, '0')

    def connects(self):
        connections_data = []
        for conn in psutil.net_connections():
            connections_data.append({
                'fd': conn.fd,
                'family': conn.family,
                'type': conn.type,
                'laddr': conn.laddr,
                'raddr': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            })
        self.send_data(connections_data, '0')
    def handle_server_request(self, command):
        if command == "cpu_ram":
            self.cpu_ram()
        elif command == "power":
            self.power()
        elif command == "battery":
            self.battery()
        elif command == "system_info":
            self.system_info()
        elif command == "processes":
            self.processes()
        elif command == "network_data":
            self.network_data()
        elif command == "storage_info":
            self.storage_info()
        elif command == "sensor_data":
            self.sensor_data()
        elif command == "io":
            self.io()
        elif command == "if_addr":
            self.if_addr()
        elif command == "connects":
             self.connects()
        else:
            print(f"Unknown command: {command}")
        #self.client_socket.close()

    # Modify start() method to receive commands from server
    def start(self):
        self.connect()
        while True:
            commands = self.client_socket.recv(4096).decode().split(";")
            for command in commands:
                if command:
                    threading.Thread(target=self.handle_server_request, args=(command,)).start()

if __name__ == "__main__":
    client = Client("localhost", 8080)
    client.start()
