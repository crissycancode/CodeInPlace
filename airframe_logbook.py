"""
The data in airframe logbook, will come from journey log and flights brough forward
"""

import pandas


def Airframe_Logbook_Headers():
    """
    Heads to display
    return: dictionary of custom headers
    """
    return {
        'DATE': 'Date', #journey log
        'CYCLES': 'Cyc', #journey log
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

def Update_Airframe_Log_Dates(journey_log, airframe_log):
    #check in journey log
    if 'DATE' not in journey_log.columns:
        raise ValueError("Column 'DATE' not found in journey_log DataFrame.")
    if 'CYCLE' not in journey_log.columns:
        raise ValueError("Column 'CYCLE' not found in journey_log DataFrame.")
    
    # check in airframe log
    if 'DATE' not in airframe_log.columns:
        raise ValueError("Column 'DATE' not found in airframe_log DataFrame.")
    
    # update airframe_log with columns from journey_log
    airframe_log = journey_log[['DATE']]
    airframe_log['CYCLES'] = journey_log['CYCLE']
    
    
    # initialize other columns to empty strings
    columns_to_initialize = [
        'TAC', 'FLT TIME Hrs', 'FLT TIME Mins', 'FLT TIME Dur', 
        'TAT Hrs', 'TAT Mins', 'TAT Dur', 'BLOCK Hrs', 'BLOCK Mins', 
        'BLOCK Dur', 'TOT BLOCK hrs', 'TOT BLOCK Mins', 'TOT BLOCK Dur'
    ]

    for col in columns_to_initialize:
        airframe_log[col] = ''
    
    # convert 'DATE' to datetime
    airframe_log['DATE'] = pandas.to_datetime(airframe_log['DATE'], errors='coerce')

    # group by 'DATE' and sum 'CYCLES'
    aggregated_data = airframe_log.groupby('DATE').agg({'CYCLES': 'sum'}).reset_index()

    # sort by 'DATE' and format it back to the desired format
    aggregated_data = aggregated_data.sort_values(by='DATE')
    aggregated_data['DATE'] = aggregated_data['DATE'].dt.strftime('%d-%b-%y')

    return aggregated_data


def Get_Cycles(data):
    pass

def Get_Total_Accumulated_Cycle():
    #total_accumulated_cycle = total_accumulated_cycle + current_cycles
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