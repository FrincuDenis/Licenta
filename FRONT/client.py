import shutil
import socket
import sys
import json
import threading
import psutil
import time
import platform
import datetime
import wmi
import winreg
from hardware import HardwareInfoCollector
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
        self.hrd = HardwareInfoCollector()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chunk_size = 4096  # Adjusted to match the server's chunk size

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            client_name = socket.gethostname()  # Get the client's computer name
            self.client_socket.send(client_name.encode())  # Send the client name to the server
            self.client_socket.send(self.get_hwid().encode())
            print(f"Connected to server at {self.host}:{self.port} as {client_name}")
        except Exception as e:
            print(f"Connection error: {e}")

    def receive_data(self):
        response = bytearray()
        end_marker = None
        while True:
            chunk = self.client_socket.recv(self.chunk_size)
            if not chunk:
                raise ConnectionError("Connection closed by client")

            response.extend(chunk)

            # Check if the terminator is in the received chunk
            if b'\0' in chunk or b'\1' in chunk:
                if b'\0' in chunk:
                    end_marker = b'\0'
                elif b'\1' in chunk:
                    end_marker = b'\1'
                break

        # Split the response at the first occurrence of the end marker
        if end_marker is not None:
            terminator_index = response.find(end_marker)
            if terminator_index != -1:
                response_data = response[:terminator_index]
            else:
                response_data = response
        else:
            response_data = response

        response_str = response_data.decode()

        if end_marker == b'\0':
            try:
                json_response = json.loads(response_str)
                if isinstance(json_response, dict):
                    for command, data in json_response.items():
                        return command, data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
            return None, None
        elif end_marker == b'\1':
            return response_str, None

        return None, None

    def handle_server_request(self):
        while True:
            try:
                command, data = self.receive_data()
                if command:
                    self.process_command(command, data)
                else:
                    print("No command received.")
            except Exception as e:
                print(f"Error handling server request: {e}")
                pass

    def process_command(self, command, data):
        command_map = {
            "get_group": self.get_group,
            "add_user": lambda: self.add_user(data[0], data[3], data[1], data[2]) if data else None,
            "remove_user": lambda: self.remove_user(data[0]) if data else None,
            "add_to_domain": lambda: self.add_to_domain(data[0], data[1], data[2]) if data else None,
            "remove_from_domain": lambda: self.remove_from_domain(data[0], data[1]) if data else None,
            "is_in_domain": self.is_in_domain,
            "fetch_all_user_info": self.fetch_all_user_info,
            "cpu_ram": self.cpu_ram,
            "power": self.power,
            "battery": self.battery,
            "system_info": self.system_info,
            "processes": self.processes,
            "storage_info": self.storage_info,
            "sensor_data": self.sensor_data,
            "network_data": self.network_data,
            "io": self.io,
            "if_addr": self.if_addr,
            "connects": self.connects,
            "shutdown": self.shutdown,
            "suspend": lambda: self.suspend_process(data),
            "resume": lambda: self.resume_process(data),
            "terminate": lambda: self.terminate_process(data),
            "kill": lambda: self.kill_process(data),
            "hardware": self.hardware,
            "installed_programs": self.installed_programs  # Add the new command here
        }

        if command in command_map:
            command_map[command]()
        else:
            print(f"Unknown command: {command}")

    def start(self):
        self.connect()
        threading.Thread(target=self.handle_server_request).start()

    def send_data(self, command, process_data):
        data_to_send = json.dumps({command: process_data})
        for i in range(0, len(data_to_send), self.chunk_size):
            chunk = data_to_send[i:i + self.chunk_size]
            self.client_socket.sendall(chunk.encode())
        self.client_socket.sendall(b'\0')

    def shutdown(self):
        self.client_socket.close()
        print("Client shutdown.")

    # Command Methods
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
        self.send_data("connects", connections_data)

    def cpu_ram(self):
        total_ram = psutil.virtual_memory().total / (1024 * 1024 * 1024)
        available_ram = psutil.virtual_memory().available / (1024 * 1024 * 1024)
        ram_usage = psutil.virtual_memory().percent
        used_ram = psutil.virtual_memory().used / (1024 * 1024 * 1024)
        ram_free = psutil.virtual_memory().free / (1024 * 1024 * 1024)
        core_count = psutil.cpu_count()
        cpu_percentage = psutil.cpu_percent(interval=1)
        main_core_count = psutil.cpu_count(logical=False)

        cpu_data = {
            "core_count": core_count,
            "cpu_percentage": cpu_percentage,
            "main_core_count": main_core_count,
            "total_ram": total_ram,
            "available_ram": available_ram,
            "ram_usage": ram_usage,
            "used_ram": used_ram,
            "ram_free": ram_free,
        }

        self.send_data("cpu_ram", cpu_data)

    def power(self):
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
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Power and sensor.Value is not None:
                            value = sensor.Value
                            if hardware.HardwareType == Hardware.HardwareType.Cpu:
                                total_cpu_power += value
                            elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd,
                                                           Hardware.HardwareType.GpuNvidia):
                                if "Vega" in hardware.Name or "Radeon Graphics" in hardware.Name or "UHD Graphics" in hardware.Name or "Iris Xe Graphics" in hardware.Name:
                                    total_igpu_power += value
                                else:
                                    total_dgpu_power += value
        except Exception as e:
            print(f"Error collecting power data: {e}")
        finally:
            computer.Close()

        power_data = {
            "cpu_power": total_cpu_power,
            "igpu_power": total_igpu_power,
            "dgpu_power": total_dgpu_power
        }

        self.send_data("power", power_data)

    def battery(self):
        battery = psutil.sensors_battery()
        battery_info = {}
        if battery is not None:
            battery_info["charge"] = round(battery.percent, 2)
            battery_info["status"] = "Charging" if battery.power_plugged and battery.percent < 100 else "Fully Charged" if battery.percent == 100 else "Discharging"
            battery_info["time_left"] = "N/A" if battery.power_plugged else self.secs2hours(battery.secsleft)
            battery_info["plugged"] = "Yes" if battery.power_plugged else "No"
        else:
            battery_info["status"] = "Platform not supported"
            battery_info["charge"] = 100
            battery_info["plugged"] = "No"
            battery_info["time_left"] = "N/A"

        self.send_data("battery", battery_info)

    def secs2hours(self, secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return f"{hh}:{mm:02d}:{ss:02d} (H:M:S)"

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

        self.send_data("system_info", system_info)

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
                    "create_time": datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                }
                process_data.append(process_info)
            except Exception as e:
                print(f"Error fetching process {pid}: {e}")

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

        computer = Hardware.Computer()
        computer.IsCpuEnabled = True
        computer.IsGpuEnabled = True
        computer.Open()

        try:
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
        except Exception as e:
            print(f"Error collecting sensor data: {e}")
        finally:
            computer.Close()

        for sensor_name, temp_values in cpu_temps.items():
            sensor_data.append({"sensor_type": "CPU", "sensor_name": sensor_name, "value": temp_values})
        for sensor_name, temp_values in gpu_temps.items():
            sensor_data.append({"sensor_type": "GPU", "sensor_name": sensor_name, "value": temp_values})

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
        self.send_data("network_data", if_stats_data)

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
        self.send_data("io", io_counters_data)

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
        self.send_data("if_addr", if_addrs_data)

    def fetch_all_user_info(self):
        self.local_account.fetch_all_user_info()
        self.send_data("fetch_all_user_info", self.local_account.all_users_info)

    def add_user(self, username, password, full_name, description):
        self.local_account.add_user(username, password, full_name, description)
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

    def get_group(self):
        self.send_data("get_group", self.local_account.get_local_groups())

    def get_hwid(self):
        c = wmi.WMI()
        hwid = None
        for system in c.Win32_ComputerSystemProduct():
            hwid = system.UUID
        return hwid

    def suspend_process(self, data):
        pid = data["pid"]
        try:
            process = psutil.Process(int(pid))
            process.suspend()
            self.send_data("suspend", {"pid": pid, "status": "suspended"})
        except Exception as e:
            self.send_data("suspend", {"pid": pid, "status": "error", "message": str(e)})

    def resume_process(self, data):
        pid = data["pid"]
        try:
            process = psutil.Process(int(pid))
            process.resume()
            self.send_data("resume", {"pid": pid, "status": "resumed"})
        except Exception as e:
            self.send_data("resume", {"pid": pid, "status": "error", "message": str(e)})

    def terminate_process(self, data):
        pid = data["pid"]
        try:
            process = psutil.Process(int(pid))
            process.terminate()
            self.send_data("terminate", {"pid": pid, "status": "terminated"})
        except Exception as e:
            self.send_data("terminate", {"pid": pid, "status": "error", "message": str(e)})

    def kill_process(self, data):
        pid = data["pid"]
        try:
            process = psutil.Process(int(pid))
            process.kill()
            self.send_data("kill", {"pid": pid, "status": "killed"})
        except Exception as e:
            self.send_data("kill", {"pid": pid, "status": "error", "message": str(e)})

    def hardware(self):
        hardware_info = self.hrd.collect_all_info("client.ps1")
        self.send_data("hardware", hardware_info)

    def installed_programs(self):
        programs = self.get_installed_programs()
        self.send_data("installed_programs", programs)

    def get_installed_programs(self):
        program_list = []

        # Registry paths to check for installed applications (32-bit and 64-bit)
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]

        for path in registry_paths:
            try:
                # Open the registry key
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)

                # Enumerate through the subkeys
                for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    sub_key = winreg.OpenKey(reg_key, sub_key_name)
                    try:
                        # Fetch the program name
                        program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                        try:
                            program_version = winreg.QueryValueEx(sub_key, "DisplayVersion")[0]
                        except FileNotFoundError:
                            program_version = "Unknown Version"
                        try:
                            install_date = winreg.QueryValueEx(sub_key, "InstallDate")[0]
                            install_date = self.format_date(install_date)
                        except FileNotFoundError:
                            install_date = "Unknown Date"
                        try:
                            publisher = winreg.QueryValueEx(sub_key, "Publisher")[0]
                        except FileNotFoundError:
                            publisher = "Unknown Publisher"
                        program_list.append({
                            "Name": program_name,
                            "Version": program_version,
                            "Install Date": install_date,
                            "Publisher": publisher
                        })
                    except FileNotFoundError:
                        # If DisplayName does not exist, skip the entry
                        continue
                    finally:
                        sub_key.Close()
                reg_key.Close()
            except FileNotFoundError:
                # If the registry path does not exist, skip it
                continue

        return program_list

    def format_date(self, date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid Date"

if __name__ == "__main__":
    client = Client("192.168.0.227", 9000)
    #client = Client("84.117.168.222", 9000)
    client.start()
