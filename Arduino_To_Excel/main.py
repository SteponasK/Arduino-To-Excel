import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from csv_to_excel_converter import CsvToExcelConverter
from csv_manager import CSVManager
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # CsvToExcelConverter.csv_to_excel(CSVManager.csv_file_name,)
