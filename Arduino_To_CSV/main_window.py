from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from serial_manager import SerialManager
from csv_manager import CSVManager
from port_manager import PortManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setupWindow()
        self.setupLabels()
        self.setupComboBox()
        self.setupStartButton()
         
        self.serial_manager = None

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

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
            
            # Start reading data from the port
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