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
        self.paused = False

    def run(self):
        with serial.Serial(port=self.port_name, baudrate=9600, timeout=1) as ser:
            while getattr(self, "running", True):
                line = ser.readline().decode().strip()
                if line:
                    self.data_received.emit(line)
                while self.paused:
                    self.sleep(1)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class MainWindow(QWidget):
    def __init__(self, ports):
        super().__init__()
        self.setWindowTitle("Egg Data To CSV")
        self.setGeometry(50, 50, 320, 200)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 220, 30)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        self.message_label = QLabel(self)
        self.message_label.setGeometry(50, 110, 220, 30)
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.message_label.setWordWrap(True)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(ports)
        self.combo_box.move(50, 80)

        self.start_button = QPushButton("Start", self)
        self.start_button.move(200, 80)
        self.start_button.clicked.connect(self.toggle_collection)

        self.serial_thread = None

    def toggle_collection(self):
        if not self.serial_thread:
            port_name = self.combo_box.currentText()
            self.label.setText(f"Selected Port: {port_name}")
            self.serial_thread = SerialThread(port_name)
            self.serial_thread.data_received.connect(self.on_data_received)
            self.serial_thread.start()
            self.start_button.setText("Stop")
            self.write_csv_title()
        else:
            self.serial_thread.running = False
            self.serial_thread.wait()
            self.serial_thread = None
            self.start_button.setText("Start")

    def write_csv_title(self):
        csv_file_name = 'kiausiniu_info.csv'
        with open(csv_file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["time", "speed"])

    def on_data_received(self, data):
        time, speed = data.split(',')
        csv_file_name = 'kiausiniu_info.csv'
        with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([int(time), float(speed)])
            message = f"Row: {int(time)}, {float(speed)} was saved"
            self.message_label.setText(message)

    def closeEvent(self, event):
        if self.serial_thread:
            self.serial_thread.running = False
            self.serial_thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ports = [port.device for port in comports()]
    window = MainWindow(ports)
    window.show()
    sys.exit(app.exec_())

