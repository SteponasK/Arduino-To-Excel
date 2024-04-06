# serial_manager.py
from PyQt5.QtCore import QObject, pyqtSignal
from serial_thread import SerialThread
from PyQt5.QtWidgets import QMessageBox

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
            # Error signal
            self.serial_thread.emit_error_signal.connect(self.handle_error)
            # Start thread
            self.serial_thread.start()

    def stop_reading(self):
        # Stop reading data from the port
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None

    def handle_error(self, error_message):
        QMessageBox.critical(None, "Error", error_message)