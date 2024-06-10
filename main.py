import pandas, csv, json, os, shutil


def Convert_To_Json(file, file_name):
    data = pandas.read_csv(file)
    data = data.dropna(axis = 1, how = 'all')

    json_data = data.to_json(orient = 'records')

    with open(file_name, 'w') as json_file:
        json_file.write(json_data)

    print(f"Successfully coverted to JSON, see {file_name}")

def Convert_To_CSV(data, filename):
    header = data[0].keys() if data else []
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header)
        writer.writeheader()
        writer.writerows(data)

def Export_CSV_To_Desktop(source_file, destination_folder):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    destination_path = os.path.join(desktop_path, destination_folder, os.path.basename(source_file))
    shutil.copy2(source_file, destination_path)

def Read_File(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def Aircraft_Directives():
    input_file = 'Aircraft_Directives.csv'
    output_file = 'Aircraft_Directives.json'
    Convert_To_Json(input_file, output_file)

def Journey_Log():
    input_file = 'Journey_Log.csv'
    output_file = 'Journey_Log.json'
    Convert_To_Json(input_file, output_file)
    data = Read_File('Journey_Log.json')
    data = Filter_Date_Total(data)
    data = Filter_Flight_Empty_Hours(data)
    data = Fill_Empty_Dates(data)
    data = Change_Value_In_Operation_Type(data)
    Convert_To_CSV(data, 'Journey_Log.csv')
    Export_CSV_To_Desktop('Journey_Log.csv', '')

#Journey_Log
def Filter_Date_Total(data_array):
    filtered_data = [data_entry for data_entry in data_array if data_entry.get("DATE") != "T0TAL"]
    return filtered_data

#Journey_Log
def Filter_Flight_Empty_Hours(data_array):
    filtered_data = [data_entry for data_entry in data_array if data_entry.get("FLIGHT_HOURS") != "0:00"]
    return filtered_data

#Journey_Log
def Fill_Empty_Dates(data):
    last_non_empty_date = None

    for data_entry in data:
        date_value = data_entry.get("DATE")
        
        if not date_value:
            if last_non_empty_date:
                data_entry["DATE"] = last_non_empty_date
        else:
            last_non_empty_date = date_value
    
    return data

#Journey_Log
def Change_Value_In_Operation_Type(data):
    for data_entry in data:
        if "OPERATION_TYPE" in data_entry:
            data_entry["OPERATION_TYPE"] = "NIGHT"
    return data

if __name__ == "__main__":
    Aircraft_Directives()
    Journey_Log()

