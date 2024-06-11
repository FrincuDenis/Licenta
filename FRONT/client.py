import shutil
import socket
import sys
import json
import threading
import psutil
import time
import platform
import datetime
from manage_pc import UserManager
import clr  # the pythonnet module
from time import sleep

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware

platforms = {
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'Mac OS',
    'win32': 'Windows',
}


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.local_account = UserManager()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chunk_size = 7168

    def connect(self):
        self.client_socket.connect((self.host, self.port))
        client_name = socket.gethostname()  # Get the client's computer name
        self.client_socket.send(client_name.encode())  # Send the client name to the server
        print(f"Connected to server at {self.host}:{self.port} as {client_name}")

    def receive_data(self):
        response = []
        end = b""
        while True:
            chunk = self.client_socket.recv(self.chunk_size)
            if chunk[-1:] == b'\0' or chunk[-1:] == b'\1':
                end=chunk[-1:]
                response.append(chunk[:-1])
                break
            response.append(chunk)
        response_data = b''.join(response).decode()
        if end == b'\0':
                try:
                    json_response = json.loads(response_data)
                    if isinstance(json_response, dict):
                        for command, data in json_response.items():
                            return command, data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                return None, None
        elif end == b'\1':
                return response_data, None

    def handle_server_request(self):
        while True:
            try:
                # First receive the command
                command,data= self.receive_data()
                # Process the command
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
                elif command == "add_user" and data:
                    self.add_user(data[0], data[3], data[1], data[2])
                elif command == "remove_user" and data:
                    self.remove_user(data[0])
                elif command == "add_to_domain" and data:
                    self.add_to_domain(data[0], data[1], data[2])
                elif command == "remove_from_domain" and data:
                    self.remove_from_domain(data[0], data[1])
                elif command == "is_in_domain":
                    self.is_in_domain()
                elif command == "fetch_all_user_info":
                    self.fetch_all_user_info()
                elif command == "shutdown":
                    self.client_socket.close()
                    return
                else:
                    print(f"Unknown command or missing data: {command}")

            except Exception as e:
                print(f"An error occurred while handling server request: {e}")
                pass

    def start(self):
        self.connect()
        threading.Thread(target=self.handle_server_request).start()

    def send_data(self, command, process_data):
        data_to_send = json.dumps({command: process_data})
        for i in range(0, len(data_to_send), self.chunk_size):
            chunk = data_to_send[i:i + self.chunk_size]
            self.client_socket.sendall(chunk.encode())
            time.sleep(0.1)
        self.client_socket.sendall(b'\0')

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
        self.send_data("connects",connections_data)

    def cpu_ram(self):
        total_ram = psutil.virtual_memory().total / (1024 * 1024 * 1024)
        available_ram = psutil.virtual_memory().available / (1024 * 1024 * 1024)
        ram_usage = psutil.virtual_memory().percent
        used_ram = psutil.virtual_memory().used / (1024 * 1024 * 1024)
        ram_free = psutil.virtual_memory().free / (1024 * 1024 * 1024)
        core = psutil.cpu_count()
        cpu_per = psutil.cpu_percent(interval=1)
        cpu_main_core = psutil.cpu_count(logical=False)

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

        self.send_data("cpu_ram",cpu_data)

    def power(self):
        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.Open()

        total_cpu_power = 0.0
        total_igpu_power = 0.0
        total_dgpu_power = 0.0

        for hardware in computer.Hardware:
            if hardware.HardwareType in (Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia,
                                         Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuIntel):
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

        self.send_data("power",power_data)

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

        self.send_data("battery",battery_info)

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

        self.send_data("system_info",system_info)

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

        self.send_data("processes", process_data)

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

        self.send_data("storage_info", storage_data)

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

            for sensor_name, temp_value in cpu_temps.items():
                sensor_data.append({"sensor_type": "CPU", "sensor_name": sensor_name, "value": temp_value})
            for sensor_name, temp_value in gpu_temps.items():
                sensor_data.append({"sensor_type": "GPU", "sensor_name": sensor_name, "value": temp_value})

        except Exception as e:
            print(f"Error initializing hardware monitor: {e}")
        finally:
            computer.Close()

        self.send_data("sensor_data", sensor_data)

    def network_data(self):
        if_stats_data = []
        for interface, stats in psutil.net_if_stats().items():
            if_stats_data.append({
                'interface': interface,
                'is_up': stats.isup,
                'duplex': stats.duplex,
                'speed': stats.speed,
                'mtu': stats.mtu
            })
        self.send_data("network_data",if_stats_data)

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
        self.send_data("io",io_counters_data)

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
        self.send_data("if_addr",if_addrs_data)

    def fetch_all_user_info(self):
        self.local_account.fetch_all_user_info()
        self.send_data("fetch_all_user_info", self.local_account.all_users_info)

    def add_user(self, username, password,full_name, description):
        self.local_account.add_user(username, password,full_name, description)
        self.send_data("add_user", {"username": username, "status": "added"})

    def remove_user(self, username):
        self.local_account.remove_user(username)
        self.send_data("remove_user", {"username": username, "status": "removed"})

    def is_in_domain(self):
        domain_status = self.local_account.is_in_domain()
        self.send_data("is_in_domain", {"is_in_domain": domain_status})

    def add_to_domain(self, domain, username, password):
        self.local_account.add_to_domain(domain, username, password)
        self.send_data("add_to_domain", {"domain": domain, "status": "added to domain"})

    def remove_from_domain(self, local_admin, local_password):
        self.local_account.remove_from_domain(local_admin, local_password)
        self.send_data("remove_from_domain", {"status": "removed from domain"})

if __name__ == "__main__":
    client = Client("192.168.31.162", 8081)
    client.start()
