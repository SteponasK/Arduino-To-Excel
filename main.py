import serial
from serial.tools.list_ports import comports
import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread

class SerialManager(QObject):
    # Signal emitted when data received from the port (multithreading)
    data_received = pyqtSignal(str)

    def __init__(self, port_name):
        super().__init__()
        # Port name to be used.
        self.port_name = port_name
        # Thread for reading data from the port
        self.serial_thread = None

    def start_reading(self):
        # Start reading data from the port
        if not self.serial_thread:
            self.serial_thread = SerialThread(self.port_name)
            self.serial_thread.data_received.connect(self.data_received)
            self.serial_thread.start()

    def stop_reading(self):
        # Stop reading data from the port
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None

class SerialThread(QThread):
    # Signal emitted when data received from the port (multithreading)
    data_received = pyqtSignal(str)

    def __init__(self, port_name):
        super().__init__()
        self.port_name = port_name
        self.paused = False

    def run(self):
        # Thread's main loop for reading data from the port
        with serial.Serial(port=self.port_name, baudrate=9600, timeout=1) as ser:
            while getattr(self, "running", True):
                line = ser.readline().decode().strip()
                if line:
                    # Emit the data (multithreading)
                    self.data_received.emit(line)
                while self.paused:
                    self.sleep(1)

    def stop(self):
        # Stop the thread
        self.running = False
        self.wait()

    def pause(self):
        # Pause the thread
        self.paused = True

    def resume(self):
        # Resume the thread
        self.paused = False

class CSVManager:
    # Name of the .csv file
    csv_file_name = 'kiausiniu_info' + '.csv'

    @staticmethod
    def write_header():
        # Write title: "time, speed" to the csv file
        with open(CSVManager.csv_file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["time", "speed"])

    @staticmethod
    def append_data(time, speed):
        # Append further data to the csv file
        with open(CSVManager.csv_file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([time, speed])

class PortManager:
    @staticmethod
    def get_ports():
        return [port.device for port in comports()]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setupWindow()
        self.setupLabels()
        self.setupComboBox()
        self.setupStartButton()
         
        self.serial_manager = None

    def setupWindow(self):
        # set up main Window UI
        self.setWindowTitle("Egg Data To CSV")
        self.setGeometry(50, 50, 320, 200)

    def setupLabels(self):
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

    def setupComboBox(self):
        # Drop-down menu for ports
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(PortManager.get_ports())
        self.combo_box.move(50, 80)

    def setupStartButton(self):
        # Button to Start/Stop proccessing data
        self.start_button = QPushButton("Start", self)
        self.start_button.move(200, 80)
        self.start_button.clicked.connect(self.toggle_collection)

    def toggle_collection(self):
        # Toggle start/stop (data collection)
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
        # Proccess & display received data 
        time, speed = map(float, data.split(','))
        CSVManager.append_data(time, speed)
        message = f"Row: {time}, {speed} was saved"
        self.message_label.setText(message)

    def closeEvent(self, event):
        # Close main window
        if self.serial_manager:
            self.serial_manager.stop_reading()
        event.accept()

if __name__ == '__main__':
    # Application instance & run event loop
    app = QApplication([])
    # Create & show window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

