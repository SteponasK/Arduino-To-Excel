import serial
from serial.tools import list_ports


ports = list_ports.comports()
print("PORTS: ", end="")
for port in ports:
    print(port.device, end=", ")
print()

if not ports:
    print("No available ports.")
    exit()

port_name = ports[0].device