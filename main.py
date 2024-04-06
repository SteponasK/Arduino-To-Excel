import serial
from serial.tools.list_ports import comports
import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt, QThread, QObject, pyqtSignal

class SerialThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port_name):
        super().__init__()
        self.port_name = port_name

    def run(self):
        with serial.Serial(port=self.port_name, baudrate=9600, timeout=1) as ser:
            while True:
                line = ser.readline().decode().strip()
                if line:
                    self.data_received.emit(line)

class MainWindow(QWidget):
    def __init__(self, ports):
        super().__init__()
        self.setWindowTitle("Egg Data To CSV")
        self.setGeometry(50, 50, 320, 200)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 220, 30)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(ports)
        self.combo_box.move(50, 80)
        self.combo_box.activated[str].connect(self.on_port_selected)

        self.serial_thread = None

    def on_port_selected(self, port_name):
        self.label.setText(f"Selected Port: {port_name}")
        self.serial_thread = SerialThread(port_name)
        self.serial_thread.data_received.connect(self.on_data_received)
        self.serial_thread.start()

    def on_data_received(self, data):
        time, speed = data.split(',')
        csv_file_name = 'kiausiniu_info.csv'
        with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([int(time), float(speed)])
            print(f"Row: {int(time)}, {float(speed)} was saved")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ports = [port.device for port in comports()]
    window = MainWindow(ports)
    window.show()
    sys.exit(app.exec_())
