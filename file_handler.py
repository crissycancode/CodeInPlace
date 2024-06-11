import pandas
import csv
# import json
import os
import shutil

class FileHandler:

    @staticmethod
    def Convert_To_Json(csv_file, json_file_name): 
        """
        Converts files with csv extension to a json [dictionary]
        Args:
            file (String): file name of the csv file
            file_name (String): file name to use for saving the json file
        """
        data = pandas.read_csv(csv_file)
        data = data.dropna(axis = 1, how = 'all')
        data = data.to_json(orient = 'records')

        with open(json_file_name, 'w') as json_file:
            json_file.write(data)

        print(f"Successfully coverted CSV file to JSON, see {json_file_name}")
    

    @staticmethod
    def Convert_To_CSV(data, filename):
        header = data[0].keys() if data else []
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = header)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def Read_File(filename):
        data = []
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data
    
    @staticmethod
    def Export_CSV_To_Desktop(source_file, destination_folder):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        destination_path = os.path.join(desktop_path, destination_folder, os.path.basename(source_file))
        shutil.copy2(source_file, destination_path)