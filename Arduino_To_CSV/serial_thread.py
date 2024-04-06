import serial
from PyQt5.QtCore import QThread, pyqtSignal

class SerialThread(QThread):
    # Signal emitted when data received from the port (multithreading)
    data_received = pyqtSignal(str)
    # Signal emitted when an error occurs (port connection)
    emit_error_signal = pyqtSignal(str)

    def __init__(self, port_name):
        super().__init__()
        self.port_name = port_name
        self.paused = False

    def run(self):
        # Thread's main loop for reading data from the port
        try:
            with serial.Serial(port=self.port_name, baudrate=9600, timeout=1) as ser:
                while getattr(self, "running", True):
                    line = ser.readline().decode().strip()
                    if line:
                        # Emit the data (multithreading)
                        self.data_received.emit(line)
                    while self.paused:
                        self.sleep(1)
        except serial.SerialException as e:
            # Create QMessageBox in the main GUI thread
            error_message = f"{e} \nPort is probably already in use"
            self.emit_error_signal.emit(error_message)

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