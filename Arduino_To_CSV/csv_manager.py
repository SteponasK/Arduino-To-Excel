import csv

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