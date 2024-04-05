import serial
from serial.tools import list_ports
import csv

ports = list_ports.comports()
print("PORTS: ", end="")
for port in ports:
    print(port.device, end=", ")
print()

if not ports:
    print("No available ports.")
    exit()

port_name = ports[0].device

arduino = serial.Serial(port=port_name, baudrate=9600, timeout=1)

first_line = "time,speed"
csv_file_name = 'kiausiniu_info.csv'
with open(csv_file_name, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(first_line.split(','))

    while True:
        newLine = arduino.readline().decode().strip()
        if(newLine == ''):
            continue
        time, speed = newLine.split(',')
        writer.writerow([int(time), float(speed)])
        print(f"Row: {int(time)}, {float(speed)} was saved")