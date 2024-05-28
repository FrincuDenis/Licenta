import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware

computer = Hardware.Computer()
computer.IsCpuEnabled = True
computer.IsGpuEnabled = True
computer.Open()

cpu_temps = {}
gpu_temps = {}
cpu_average_temp = None
tjmax_temps = {}

# Iterate through hardware components
for hardware in computer.Hardware:
    if hardware.HardwareType in (
            Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd,
            Hardware.HardwareType.GpuIntel):
        hardware.Update()
        for sensor in hardware.Sensors:
            # Exclude power sensors
            if sensor.SensorType == Hardware.SensorType.Temperature:
                temp_value = sensor.Value
                sensor_name = sensor.Name
                # Handle CPU Average sensor specifically
                if hardware.HardwareType == Hardware.HardwareType.Cpu:
                    if sensor_name == "CPU Average":
                        cpu_average_temp = temp_value
                    elif "Tjmax" in sensor_name:
                        if sensor_name not in tjmax_temps:
                            tjmax_temps[sensor_name] = [temp_value]
                        else:
                            tjmax_temps[sensor_name].append(temp_value)
                    else:
                        if sensor_name not in cpu_temps:
                            cpu_temps[sensor_name] = [temp_value]
                        else:
                            cpu_temps[sensor_name].append(temp_value)
                # Gather GPU temperature readings
                elif hardware.HardwareType in (Hardware.HardwareType.GpuIntel, Hardware.HardwareType.GpuAmd, Hardware.HardwareType.GpuNvidia):
                    if "Tjmax" in sensor_name:
                        if sensor_name not in tjmax_temps:
                            tjmax_temps[sensor_name] = [temp_value]
                        else:
                            tjmax_temps[sensor_name].append(temp_value)
                    else:
                        if sensor_name not in gpu_temps:
                            gpu_temps[sensor_name] = [temp_value]
                        else:
                            gpu_temps[sensor_name].append(temp_value)

computer.Close()

# Calculate minimum, maximum, and average CPU temperature readings per sensor
cpu_min_temp = min([min(temp_list) for temp_list in cpu_temps.values()])
cpu_max_temp = max([max(temp_list) for temp_list in cpu_temps.values()])

# Calculate minimum, maximum, and average GPU temperature readings per sensor
gpu_min_temp = min([min(temp_list) for temp_list in gpu_temps.values()])
gpu_max_temp = max([max(temp_list) for temp_list in gpu_temps.values()])

# Calculate average GPU temperature across all sensors
total_gpu_temp = sum([sum(temp_list) for temp_list in gpu_temps.values()])
num_gpu_sensors = sum([len(temp_list) for temp_list in gpu_temps.values()])
avg_gpu_temp = total_gpu_temp / num_gpu_sensors

# Calculate average temperature per Tjmax sensor
tjmax_avg_temps = {sensor_name: sum(temp_list) / len(temp_list) for sensor_name, temp_list in tjmax_temps.items()}

print("CPU Temperatures:")
for sensor_name, temps in cpu_temps.items():
    current_temp = temps[-1]
    avg_temp = sum(temps) / len(temps)
    print(f"{sensor_name}: Current: {current_temp:.2f} °C, Min: {min(temps):.2f} °C, Max: {max(temps):.2f} °C, Avg: {avg_temp:.2f} °C")
if cpu_average_temp is not None:
    print(f"CPU Average: {cpu_average_temp:.2f} °C")

print("\nGPU Temperatures:")
for sensor_name, temps in gpu_temps.items():
    current_temp = temps[-1]
    avg_temp = sum(temps) / len(temps)
    print(f"{sensor_name}: Current: {current_temp:.2f} °C, Min: {min(temps):.2f} °C, Max: {max(temps):.2f} °C, Avg: {avg_temp:.2f} °C")

print(f"\nOverall GPU Average Temperature: {avg_gpu_temp:.2f} °C")

print("\nTjmax Temperatures:")
for sensor_name, temps in tjmax_temps.items():
    current_temp = temps[-1]
    avg_temp = sum(temps) / len(temps)
    print(f"{sensor_name}: Current: {current_temp:.2f} °C, Avg: {avg_temp:.2f} °C")


