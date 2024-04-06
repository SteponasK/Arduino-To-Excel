import serial
from serial.tools.list_ports import comports
import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread

class SerialManager(QObject):
    data_received = pyqtSignal(str)

    def __init__(self, port_name):
        super().__init__()
        self.port_name = port_name
        self.serial_thread = None

    def start_reading(self):
        if not self.serial_thread:
            self.serial_thread = SerialThread(self.port_name)
            self.serial_thread.data_received.connect(self.data_received)
            self.serial_thread.start()

    def stop_reading(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None

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

    def stop(self):
        self.running = False
        self.wait()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class CSVManager:
    @staticmethod
    def write_header():
        csv_file_name = 'kiausiniu_info.csv'
        with open(csv_file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["time", "speed"])

    @staticmethod
    def append_data(time, speed):
        csv_file_name = 'kiausiniu_info.csv'
        with open(csv_file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([time, speed])

class PortManager:
    @staticmethod
    def get_ports():
        return [port.device for port in comports()]

class MainWindow(QWidget):
    def __init__(self, ports):
        super().__init__()
        # set up main Window UI
        self.setWindowTitle("Egg Data To CSV")
        self.setGeometry(50, 50, 320, 200)

        # Label for selected port info
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 220, 30)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)

        # Label for status message (if line was saved)
        self.message_label = QLabel(self)
        self.message_label.setGeometry(50, 110, 220, 30)
        self.message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.message_label.setWordWrap(True)

        # Drop-down menu for ports
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(ports)
        self.combo_box.move(50, 80)

        # Button to Start/Stop proccessing data
        self.start_button = QPushButton("Start", self)
        self.start_button.move(200, 80)
        self.start_button.clicked.connect(self.toggle_collection)

        self.serial_manager = None

    def toggle_collection(self):
        if not self.serial_manager:
            port_name = self.combo_box.currentText()
            self.label.setText(f"Selected Port: {port_name}")
            self.serial_manager = SerialManager(port_name)
            self.serial_manager.data_received.connect(self.on_data_received)
            self.serial_manager.start_reading()
            self.start_button.setText("Stop")
            CSVManager.write_header()
        else:
            self.serial_manager.stop_reading()
            self.serial_manager = None
            self.start_button.setText("Start")

    def on_data_received(self, data):
        time, speed = map(float, data.split(','))
        CSVManager.append_data(time, speed)
        message = f"Row: {time}, {speed} was saved"
        self.message_label.setText(message)

    def closeEvent(self, event):
        if self.serial_manager:
            self.serial_manager.stop_reading()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    ports = [port.device for port in comports()]
    window = MainWindow(ports)
    window.show()
    sys.exit(app.exec_())

