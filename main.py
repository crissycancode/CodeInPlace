from tabulate import tabulate
from file_handler import  Read_File, Convert_To_CSV, Convert_To_Json, Export_CSV_To_Desktop
from journey_log_cleaner import (Forward_Fill_Empty_Dates, 
                                 Remove_Total_Summary_Rows, 
                                 Remove_Empty_Cycle, 
                                 Fill_In_Flight_Hours, 
                                 Fill_In_Block_Time, 
                                 Fill_In_Total_Flying_Hours, 
                                 Fill_In_Total_Block_Time,
                                 Flight_Hours_In_Hours)

def Airworthiness_Directives():
    input_file = 'Airworthiness_Directives.csv'
    output_file = 'Airworthiness_Directives.json'
    # Convert_To_Json(input_file, output_file)

def Journey_Log():
    
    data = Read_File('Journey_Log.csv') #read the file
    #customizations start here
    data = Remove_Total_Summary_Rows(data) #remove the rows with values for 'computing total summary'
    data = Remove_Empty_Cycle(data) #remove nan cycles
    data = Forward_Fill_Empty_Dates(data) #forward fill nan dates
    # data = Fill_In_Flight_Hours(data) #start modifying this
    data = Fill_In_Block_Time(data)
    data = Fill_In_Total_Flying_Hours(data)
    data = Fill_In_Total_Block_Time(data)
    data = Flight_Hours_In_Hours(data)

    #table starts here
    header_mapping = {
        "DATE": "Date",
        "OPERATION": "Op",
        "SECTOR FROM": "From",
        "SECTOR TO": "To",
        "OFF BLOCKS": "OffB",
        "TAKE OFF": "TO",
        "ON GROUND": "OG",
        "ON BLOCKS": "OnB",
        "CYCLE": "Cyc",
        "FH(HOURS)": "FH\nHrs",
        "FH(MINUTES)": "FH\nMins",
        "FLIGHT HOURS": "FH",
        "BT(HOURS)": "BT\nHrs",
        "BT(MINUTES)": "BT\nMins",
        "BLOCK TIME": "BT",
        "TFH(HOURS)": "TFH\nHrs",	
        "TFH(MINUTES)": "TFH\nMins",
        "TOTAL FLYING HOURS": "Tot FH",
        "TOTB(HOURS)": "TotB\nHrs",	
        "TOTB(MINUTES)": "TotB\nMins",
        "TOTAL BLOCK TIME": "Tot BT",
        "TOTAL CYCLE": "Tot C"
    }
    # columns_to_hide = ["FH(HOURS)", "FH(MINUTES)","BT(HOURS)","BT(MINUTES)","TFH(HOURS)","TFH(MINUTES)","TOTB(HOURS)","TOTB(MINUTES)"]
    # columns_to_hide = ["FLIGHT HOURS", "BLOCK TIME","TOTAL FLYING HOURS","TOTAL BLOCK TIME"]
    # data = data.drop(columns = columns_to_hide)

    default_header = data.columns
    new_headers = [header_mapping.get(header, header) for header in default_header]

    #creates stylizes table similar to 'prettytable'
    pretty_table = tabulate(data, headers = new_headers, showindex = False, tablefmt = 'pretty')
    print(pretty_table) #prints the table to console

    
    

def Foo():
    # Use these functions for file exports
    # Convert_To_CSV(data, 'Journey_Log.csv') #modified data
    # input_filename = 'Journey_Log.csv' #string for input filename
    # output_filename = 'Journey_Log.json' #string for output filename
    # Convert_To_Json(input_filename, output_filename)
    # Export_CSV_To_Desktop('Journey_Log.csv', '') #remove this later
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
    Journey_Log() #finished
    # Logbook()

    

if __name__ == "__main__":
    Main()

