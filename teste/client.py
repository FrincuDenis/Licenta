import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware


computer = Hardware.Computer()
computer.IsCpuEnabled = True
computer.IsGpuEnabled = True
computer.Open()

for hardware in computer.Hardware:
    if hardware.HardwareType == Hardware.HardwareType.Cpu or hardware.HardwareType == Hardware.HardwareType.GpuNvidia or hardware.HardwareType == Hardware.HardwareType.GpuAmd:
        hardware.Update()
        for sensor in hardware.Sensors:
            if sensor.SensorType == Hardware.SensorType.Power:
                value="{:.2f}".format(sensor.Value)
                print(f"{hardware.Name} - {sensor.Name}: {value} ")

computer.Close()