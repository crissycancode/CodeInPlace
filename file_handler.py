import pandas
import csv
import os
import shutil

def Read_File(filename):
    data_frame = pandas.read_csv(filename)
    return data_frame

def Convert_To_Json(csv_file, json_file_name): 
    """
    Converts files with csv extension to a json [dictionary]
    Args:
        csv_file (String): file name of the csv file
        json_file_name (String): file name to use for saving the json file
    """
    data = pandas.read_csv(csv_file)
    data = data.dropna(axis = 1, how = 'all')
    data = data.to_json(orient = 'records')

    with open(json_file_name, 'w') as json_file:
        json_file.write(data)

    print(f"Successfully converted CSV file to JSON, see {json_file_name}")


def Convert_To_CSV(data, csv_file_name):
    """
    save file to csv format
    """
    if not data.empty:
            data.to_csv(csv_file_name, index = False)

def Export_CSV_To_Desktop(source_file, destination_folder):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    destination_path = os.path.join(desktop_path, destination_folder, os.path.basename(source_file))
    shutil.copy2(source_file, destination_path)

