from serial.tools.list_ports import comports

class PortManager:
    @staticmethod
    def get_ports():
        return [port.device for port in comports()]