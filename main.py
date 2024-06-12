# from file_handler import FileHandler
from file_handler import Convert_To_CSV, Convert_To_Json, Read_File, Export_CSV_To_Desktop

def Airworthiness_Directives():
    input_file = 'Airworthiness_Directives.csv'
    output_file = 'Airworthiness_Directives.json'
    Convert_To_Json(input_file, output_file)

def Journey_Log():
    input_filename = 'Journey_Log.csv' #string for input filename
    output_filename = 'Journey_Log.json' #string for output filename

    data = Read_File('Journey_Log.csv') #file to read
    #formatings
    data = Filter_Date_Total(data)
    data = Filter_Flight_Empty_Hours(data)
    data = Fill_Empty_Dates(data)
    data = Change_Value_In_Operation_Type(data)
    
    Convert_To_CSV(data, 'Journey_Log.csv') #modified data
    Convert_To_Json(input_filename, output_filename)
    Export_CSV_To_Desktop('Journey_Log.csv', '') #remove this later

def Hard_Time():
    pass

def Logbook():
    #call Airframe_Logbook(), Right_Hand_Engine_Logbook(), and Right_Hand_Engine_Logbook() from here
    pass

def Airframe_Logbook():
    pass

def Left_Hand_Engine_Logbook():
    pass

def Right_Hand_Engine_Logbook():
    pass

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

            #somthing
    return data

def Main():
    # Airworthiness_Directives()
    Journey_Log()

if __name__ == "__main__":
    Main()

