from prettytable import PrettyTable
from file_handler import  Read_File,  Remove_Column_From_Data, Convert_To_CSV, Convert_To_Json, Export_CSV_To_Desktop
from journey_log_cleaner import Backfill_Empty_Dates, Remove_Total_Summary_Rows, Remove_Empty_Flight_Hours, Standardize_Operation_Type, Fill_In_Flight_Hours, Fill_In_Block_Time, Fill_In_Total_Flying_Hours, Fill_In_Total_Block_Time

def Airworthiness_Directives():
    input_file = 'Airworthiness_Directives.csv'
    output_file = 'Airworthiness_Directives.json'
    # Convert_To_Json(input_file, output_file)

def Journey_Log():
    
    data = Read_File('Journey_Log.csv') #file to read
    data = Fill_In_Flight_Hours(data) #fillin the flight hours using values in FH(HOURS) and FH(MINUTES)
    data = Remove_Empty_Flight_Hours(data) #remove blank flight hours
    data = Backfill_Empty_Dates(data) #assign dates
    data = Remove_Total_Summary_Rows(data) #remove the rows with values for computing total summary
    data = Standardize_Operation_Type(data) #night operation with "Night" and leave day operation with "-"
    data = Remove_Column_From_Data(data, "FH(HOURS)") #no longer needed after filling in the flight hours
    data = Remove_Column_From_Data(data, "FH(MINUTES)") #no longer needed after filling in the flight hours
    data = Fill_In_Block_Time(data)
    data = Remove_Column_From_Data(data, "BT(HOURS)") #no longer needed after filling in the block time
    data = Remove_Column_From_Data(data, "BT(MINUTES)") #no longer needed after filling in the block time
    data = Fill_In_Total_Flying_Hours(data)
    data = Remove_Column_From_Data(data, "TFH(HOURS)") #no longer needed after filling in the block time
    data = Remove_Column_From_Data(data, "TFH(MINUTES)") #no longer needed after filling in the block time
    data = Fill_In_Total_Block_Time(data)
    data = Remove_Column_From_Data(data, "TOTB(HOURS)") #no longer needed after filling in the block time
    data = Remove_Column_From_Data(data, "TOTB(MINUTES)") #no longer needed after filling in the block time

    table = Create_Pretty_Table(data)
    print(table)
    
    # Convert_To_CSV(data, 'Journey_Log.csv') #modified data
    # input_filename = 'Journey_Log.csv' #string for input filename
    # output_filename = 'Journey_Log.json' #string for output filename
    # Convert_To_Json(input_filename, output_filename)
    # Export_CSV_To_Desktop('Journey_Log.csv', '') #remove this later


def Create_Pretty_Table(data):
    table = PrettyTable()
    table.max_width = 150  # Adjust as needed
    if data:
        header = data[0].keys()
        table.field_names = header #must be unique
        for row in data:
            table.add_row(row.values())
    return table

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

