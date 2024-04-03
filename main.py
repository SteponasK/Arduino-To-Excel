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

arduino = serial.Serial(port_name, 9600, 1)

first_line = arduino.readline().decode().strip()

newLines = []
while True:
    newLines.append(arduino.readline().decode().strip())
    