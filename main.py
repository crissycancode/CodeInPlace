# from file_handler import FileHandler
from file_handler import Convert_To_CSV, Convert_To_Json, Read_File, Export_CSV_To_Desktop
from journey_log_cleaner import Backfill_Empty_Dates, Remove_Total_Summary_Rows, Remove_Empty_Flight_Hours, Standardize_Operation_Type

def Airworthiness_Directives():
    input_file = 'Airworthiness_Directives.csv'
    output_file = 'Airworthiness_Directives.json'
    Convert_To_Json(input_file, output_file)

def Journey_Log():
    input_filename = 'Journey_Log.csv' #string for input filename
    output_filename = 'Journey_Log.json' #string for output filename
    data = Read_File('Journey_Log.csv') #file to read
    #Formatting
    # data = Remove_Empty_Flight_Hours(data)
    data = Backfill_Empty_Dates(data)
    data = Remove_Total_Summary_Rows(data) #remove non date
    data = Standardize_Operation_Type(data)
    
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

def Main():
    # Airworthiness_Directives()
    Journey_Log()

if __name__ == "__main__":
    Main()

