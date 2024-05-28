import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware

computer = Hardware.Computer()
computer.IsCpuEnabled = True
computer.IsGpuEnabled = True
computer.Open()

total_cpu_power = 0.0
total_igpu_power = 0.0
total_dgpu_power = 0.0
amd=["Radeon HD",]
# Iterate through hardware components
for hardware in computer.Hardware:
    if hardware.HardwareType in (
    Hardware.HardwareType.Cpu, Hardware.HardwareType.GpuNvidia, Hardware.HardwareType.GpuAmd,
    Hardware.HardwareType.GpuIntel):
        hardware.Update()
        for sensor in hardware.Sensors:
            if sensor.SensorType == Hardware.SensorType.Power:
                value = sensor.Value
                formatted_value = "{:.2f}".format(value)
                print(f"{hardware.Name} - {sensor.Name}: {formatted_value} ")

                # Sum the CPU power values
                if hardware.HardwareType == Hardware.HardwareType.Cpu:
                    total_cpu_power += value
                # Identify iGPU and dGPU power values for Intel and AMD
                elif hardware.HardwareType == Hardware.HardwareType.GpuIntel:
                    if "UHD" in hardware.Name or "Iris" in hardware.Name:
                        total_igpu_power += value
                    else:
                        total_dgpu_power += value
                elif hardware.HardwareType == Hardware.HardwareType.GpuAmd:
                    if "Vega" in hardware.Name or "Radeon Graphics" in hardware.Name or "M" in hardware.Name or "S" in hardware.Name:
                        total_igpu_power += value
                    else:
                        total_dgpu_power += value
                # Sum the dGPU power values for Nvidia
                elif hardware.HardwareType == Hardware.HardwareType.GpuNvidia:
                    total_dgpu_power += value

computer.Close()

print("Total CPU Power: {:.2f}".format(total_cpu_power))
print("igpu power: {:.2f}".format(total_igpu_power))
print("dgpu power: {:.2f}".format(total_dgpu_power))