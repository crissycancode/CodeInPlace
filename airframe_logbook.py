"""
The data in airframe logbook, will come from journey log and flights brough forward
"""

import pandas
from time_utils import (Convert_To_Datetime)


def Airframe_Logbook_Headers():
    """
    Heads to display
    return: dictionary of custom headers
    """
    return {
        'DATE': 'Date', #journey log
        'CYCLE': 'Cyc', #journey log
        'TAC': 'TAC',	#totals broght forward 
        'FLT TIME Hrs': 'FH\nHrs', #journey log
        'FLT TIME Hrs': 'FH\nMins', #journey log
        'FLT TIME Dur': 'FH', #journey log
        'TAT Hrs': 'TAT\nHrs', #totals broght forward 
        'TAT Mins': 'TAT\nMins', #totals broght forward 
        'TAT Dur': 'TAT\nDur', #totals broght forward 
        'BLOCK Hrs': 'BT\nHrs', #journey log
        'BLOCK Mins': 'BT\nMins', #journey log
        'BLOCK Dur': 'BT', #journey log
        'TOT BLOCK hrs': 'TotB\nHrs', #journey log
        'TOT BLOCK Mins': 'TotB\nMins',	#journey log
        'TOT BLOCK Dur': 'TotB' #journey log
    }

#'TAC AF' 'TAT AF Hrs' 'TAT AF Mins' 'TAT AF Dur' (totals brought forward)
# get computations for each values in header mapping

def Validate_Columns(columns,data_frame, file_name): #will posible be used to the other logs
    """
    Check if the colum exist in the data frame
    Args:
        columns: string array of column headers
        data_frame: data
        file_name[string]: data from title
    Return:
        Boolean value
    """
    for column in columns:
        if column not in data_frame.columns:
            raise ValueError(f"Column '{column}' not found in {file_name} DataFrame.")
    
def Update_Airframe_Log_Dates(journey_log, airframe_log):
    #check column in journey log
    journey_log_columns = ['DATE', 'CYCLE']
    Validate_Columns(journey_log_columns, journey_log, 'journey_log')

    airframe_log_columns = ['DATE', 'CYCLE']
    Validate_Columns(airframe_log_columns, airframe_log, 'airframe_log')
    
    # update airframe_log (date, cycle) with values from journey_log
    airframe_log = journey_log[['DATE']].copy()
    airframe_log.loc[:, 'DATE'] = Convert_To_Datetime(airframe_log['DATE'])
    airframe_log.loc[:, 'CYCLE'] = journey_log['CYCLE']

    # group by 'DATE', then sum 'CYCLE' by date
    aggregated_data = airframe_log.groupby('DATE').agg({'CYCLE': 'sum'}).reset_index()
    # sort by 'DATE'
    aggregated_data = aggregated_data.sort_values(by='DATE')
    # format to day-month-year
    aggregated_data['DATE'] = aggregated_data['DATE'].dt.strftime('%d-%b-%y')

    return aggregated_data


def Get_Cycles(data):
    pass

def Get_Total_Accumulated_Cycle():
    #(TAC) for an aircraft or engine refers to the cumulative count of flight cycles since the component was first put into service.
    #This means 'Flight Brought Forward' is now needed along with Journey Log
    #Total_accumulated_cycle = total_accumulated_cycle + current_cycles
    pass

def Get_Total_Airframe_Time(): #(Duration)
    #func for hours, mins
    #total_airframe_time = total_airframe_time + current_flight_hours
    pass

def Get_Flight_Time():#(Duration)
    #func for hours, mins
    pass

def Get_Block_Time():#(Duration)
    #func for hours, mins
    pass

def Get_Total_Block_Time():#(Duration)
    #func for hours, mins
    pass