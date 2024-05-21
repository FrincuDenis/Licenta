import clr
import socket
import time

clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

# Initialize Computer object
c = Computer()
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

# Define server parameters
HOST = '127.0.0.1'  # Server IP address
PORT = 65432  # Server port
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    for a in range(0, len(c.Hardware[0].Sensors)):
        if "/amdcpu/0/power/0" in str(c.Hardware[0].Sensors[a].Identifier):
            cpu_value = c.Hardware[0].Sensors[a].get_Value()
            if cpu_value is not None:
                cpu_value = "{:.2f}".format(cpu_value)
            c.Hardware[0].Update()

    for a in range(0, len(c.Hardware[1].Sensors)):
        if "/atigpu/0/power/0" in str(c.Hardware[1].Sensors[a].Identifier):
            gpu_value = c.Hardware[1].Sensors[a].get_Value()
            if gpu_value is not None:
                gpu_value = "{:.2f}".format(gpu_value)
            c.Hardware[1].Update()

    # Send data to the server
    if cpu_value is not None:
        data = f'{cpu_value},{gpu_value}'.encode()
        client_socket.sendall(data)

        print('Data sent to server:', data.decode())

    time.sleep(1)  # Sleep to avoid busy-waiting
