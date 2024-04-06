import serial
from serial.tools.list_ports import comports
import csv

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
def window(ports):
   app = QApplication(sys.argv)
   widget = QWidget()
   widget.setGeometry(50,50,320,200)
   widget.setWindowTitle("Egg Data To CSV")

   label = QLabel(widget)
   label.move(40,50)
   label.setGeometry(50, 50, 220, 30)
   label.setAlignment(Qt.AlignLeft | Qt.AlignTop) 
   label.setWordWrap(True) 


   combo_box = QComboBox(widget)
   combo_box.addItems(ports)
   combo_box.move(50, 80)
   combo_box.activated[str].connect(lambda text: on_port_selected(text, label))

   widget.show()
   sys.exit(app.exec_())


def on_port_selected(port_name, label):
    label.setText(f"Selected Port: {port_name}")
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
if __name__ == '__main__':
   ports = [port.device for port in comports()]
   window(ports)