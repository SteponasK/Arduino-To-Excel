import csv
from openpyxl import Workbook

class CsvToExcelConverter():
    @staticmethod
    def csv_to_excel(csv_file, excel_file):
        # Creating workbook & selecting the worksheet
        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            
            # Writing values in the worksheet
            for row_index, row in enumerate(csv_reader, start=1):
                for column_index, value in enumerate(row, start=1):
                    ws.cell(row=row_index, column=column_index).value = value

        wb.save(excel_file)
