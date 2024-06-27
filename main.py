from tabulate import tabulate
from file_handler import  Read_File, Convert_To_CSV, Convert_To_Json, Export_CSV_To_Desktop
from journey_log_cleaner import (Update_Empty_Flight_Dates, 
                                 Remove_Total_Summary_Rows, 
                                 Remove_Empty_Cycle, 
                                 Update_Flight_Hours,
                                 Update_Block_Time,
                                 Update_Total_Cycle,
                                 Journey_Log_Headers)
from airframe_logbook import (Airframe_Logbook_Headers,
                              Aggregate_Data,
                              Create_Airframe_Log,
                              Reference_Cycles_From_Journey_Log,
                              Add_Total_Accumulated_Cycle,
                              Add_Flying_Time_In_Hours,
                              Add_Flying_Time_In_Minutes,
                              Add_Flying_Time_Duration,
                              Add_Total_Airframe_Time,
                              Add_Total_Airframe_Time_In_Hours,
                              Add_Total_Airframe_Time_In_Minutes,
                              Add_Block_Time,
                              Add_Block_Time_In_Hours,
                              Add_Block_Time_In_Minutes,
                              Add_Total_Block_Time,
                              Add_Total_Block_Time_In_Hours,
                              Add_Total_Block_Time_In_Minutes)


def Airworthiness_Directives():
    input_file = 'Airworthiness_Directives.csv'
    output_file = 'Airworthiness_Directives.json'
    # Convert_To_Json(input_file, output_file)


def Journey_Log():
    print(f"Journey Log")
    data = Read_File('Journey_Log.csv') #assign csv to data
    data = Remove_Total_Summary_Rows(data) #remove the rows with values for 'computing total summary'
    data = Remove_Empty_Cycle(data) #remove nan cycles
    data = Update_Empty_Flight_Dates(data) #forward fill nan dates
    data = Update_Block_Time(data)
    data = Update_Flight_Hours(data)
    data = Update_Total_Cycle(data)

    Convert_To_CSV(data, 'updated_journey_log.csv') #once this is converted to csv, it will be used by airframe logbook
    headers = Journey_Log_Headers()
    Print_Data_To_Console(data, headers)


def Airframe_Logbook():
    print(f"Airframe Log")
    journey_log = Read_File('updated_journey_log.csv')
    totals_brought_forward = Read_File('flights_brought_forward.csv')

    airframe_data = Create_Airframe_Log(journey_log)
    airframe_data = Reference_Cycles_From_Journey_Log(journey_log, airframe_data)
    airframe_data = Add_Total_Accumulated_Cycle(totals_brought_forward, airframe_data)
    airframe_data = Add_Flying_Time_In_Hours(journey_log, airframe_data)
    airframe_data = Add_Flying_Time_In_Minutes(journey_log, airframe_data)
    airframe_data = Add_Flying_Time_Duration(journey_log, airframe_data)
    airframe_data = Add_Total_Airframe_Time(journey_log, totals_brought_forward, airframe_data)
    airframe_data = Add_Total_Airframe_Time_In_Hours(journey_log, totals_brought_forward, airframe_data)
    airframe_data = Add_Total_Airframe_Time_In_Minutes(journey_log, totals_brought_forward, airframe_data)
    airframe_data = Add_Block_Time(journey_log, airframe_data)
    airframe_data = Add_Block_Time_In_Hours(journey_log, airframe_data)
    airframe_data = Add_Block_Time_In_Minutes(journey_log, airframe_data)
    airframe_data = Add_Total_Block_Time(journey_log, airframe_data)
    airframe_data = Add_Total_Block_Time_In_Hours(journey_log, airframe_data)
    airframe_data = Add_Total_Block_Time_In_Minutes(journey_log, airframe_data)

    airframe_data = Aggregate_Data(airframe_data) #do this last, since it is sorting
    header_map  = Airframe_Logbook_Headers()
    
    Print_Data_To_Console(airframe_data, header_map)


def Left_Hand_Engine_Logbook():
    pass


def Right_Hand_Engine_Logbook():
    pass


def Print_Data_To_Console(data, mapped_header):
    default_header = data.columns #default column-headers
    new_headers = [mapped_header.get(header, header) for header in default_header]
    pretty_table = tabulate(data, headers = new_headers, showindex = False, tablefmt = 'pretty')
    print(pretty_table) #prints the table to console


def Hide_Columns(data, columns):
    # columns = ["FH(HOURS)", "FH(MINUTES)","BT(HOURS)","BT(MINUTES)","TFH(HOURS)","TFH(MINUTES)","TOTB(HOURS)","TOTB(MINUTES)"]
    # columns = ["FLIGHT HOURS", "BLOCK TIME","TOTAL FLYING HOURS","TOTAL BLOCK TIME"]
    # return data.drop(columns = columns_to_hide)
    pass


def Foo():
    # Use these functions for file exports
    # Convert_To_CSV(data, 'Journey_Log.csv') #modified data
    # input_filename = 'Journey_Log.csv' #string for input filename
    # output_filename = 'Journey_Log.json' #string for output filename
    # Convert_To_Json(input_filename, output_filename)
    # Export_CSV_To_Desktop('Journey_Log.csv', '') #remove this later
    pass


def Main():
    # Airworthiness_Directives()
    Journey_Log() #finished
    #logbooks
    Airframe_Logbook()


if __name__ == "__main__":
    Main()

