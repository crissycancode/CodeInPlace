from time_utils import (Convert_To_Datetime)
import pandas

#'TAC AF' 'TAT AF Hrs' 'TAT AF Mins' 'TAT AF Dur' (totals brought forward)
# get computations for each values in header mapping

def Validate_Columns(columns,data_frame, file_name): #will posible be used to the other logs
    """
    Check if the colum exist in the data frame
    Args:
        columns: string array of column headers
        data_frame: data
        file_name[string]: data from title
    """
    for column in columns:
        if column not in data_frame.columns:
            raise ValueError(f"Column '{column}' not found in {file_name} DataFrame.")


def Aggregate_Data(airframe_log):
    # group by 'DATE', then sum 'CYCLE' by date
    airframe_log.loc[:, 'DATE'] = Convert_To_Datetime(airframe_log['DATE'])

    aggregated_data = airframe_log.groupby('DATE').agg({
        'CYCLE': 'sum', #sum the 'CYCLE'
        'TAC': 'last',#retain the first 'TAC' value
        'FLT TIME Hrs': 'last',
        'FLT TIME Mins': 'last',
        'FLT TIME Dur': 'last',
        'TAT Hrs': 'last',
        'TAT Mins': 'last',
        'TAT Dur': 'last',
        'BLOCK Hrs': 'last',
        'BLOCK Mins': 'last',
        'BLOCK Dur': 'last',
        'TOT BLOCK Hrs': 'last',
        'TOT BLOCK Mins': 'last',
        'TOT BLOCK Dur': 'last'
    }).reset_index()

    # sort by 'DATE'
    aggregated_data = aggregated_data.sort_values(by = 'DATE')
    # format to day-month-year
    aggregated_data['DATE'] = aggregated_data['DATE'].dt.strftime('%d-%b-%y')

    return aggregated_data

def Create_Airframe_Log(journey_log):
    airframe_log = journey_log.loc[:, ['DATE']]
    return airframe_log

def Reference_Cycles_From_Journey_Log(journey_log, airframe_data):
    airframe_data.loc[:, 'CYCLE'] = journey_log['CYCLE']
    return airframe_data

def Add_Total_Accumulated_Cycle(totals_brought_forward, airframe_data):
    #(TAC) for an aircraft or engine refers to the cumulative count of flight cycles since the component was first put into service.
    #This means 'Flight Brought Forward' is now needed along with Journey Log
    #Total_accumulated_cycle = total_accumulated_cycle + current_cycles
    tac = totals_brought_forward['TAC AF'][0]
    cycle = airframe_data['CYCLE'].cumsum()
    airframe_data['TAC'] = tac + cycle
    return airframe_data

def Add_Flying_Time_In_Hours(journey_log, airframe_data):
    airframe_data.loc[:,'FLT TIME Hrs'] = journey_log['FH(HOURS)']
    return airframe_data

def Add_Flying_Time_In_Minutes(journey_log, airframe_data):
    airframe_data.loc[:,'FLT TIME Mins'] = journey_log['FH(MINUTES)']
    return airframe_data

def Add_Flying_Time_Duration(journey_log, airframe_data):
    # 'FLT TIME Dur': 'FH', #journey log
    airframe_data.loc[:,'FLT TIME Dur'] = journey_log['FLIGHT HOURS']
    return airframe_data

def Add_Total_Airframe_Time(journey_log, totals_brought_forward, airframe_data):
    tat_hours = totals_brought_forward['TAT AF Hrs'][0] * 60
    tat_minutes = totals_brought_forward['TAT AF Mins'][0]
    tat  = tat_hours + tat_minutes
    flight_hours = journey_log['FLIGHT HOURS'].cumsum()

    tat = tat + flight_hours
    airframe_data.loc[:,'TAT Dur'] = tat.astype(int)
    return airframe_data # in minutes

def Add_Total_Airframe_Time_In_Hours(journey_log, totals_brought_forward, airframe_data):
    tat_hours = totals_brought_forward['TAT AF Hrs'][0]
    flight_hours = journey_log['FH(HOURS)'].cumsum()
    tat_hours = tat_hours + flight_hours
    airframe_data.loc[:,'TAT Hrs'] = tat_hours.astype(int)
    return airframe_data

def Add_Total_Airframe_Time_In_Minutes(journey_log, totals_brought_forward, airframe_data):
    tat_mins = totals_brought_forward['TAT AF Mins'][0]
    flight_mins = journey_log['FH(MINUTES)'].cumsum()
    tat_mins = tat_mins + flight_mins
    airframe_data.loc[:,'TAT Mins'] = tat_mins.astype(int)
    return airframe_data

def Add_Block_Time(journey_log, airframe_data):
    airframe_data.loc[:,'BLOCK Dur'] = journey_log['BLOCK TIME']
    return airframe_data

def Add_Block_Time_In_Hours(journey_log, airframe_data):
    airframe_data.loc[:,'BLOCK Hrs'] = journey_log['BT(HOURS)']
    return airframe_data

def Add_Block_Time_In_Minutes(journey_log, airframe_data):
    airframe_data.loc[:,'BLOCK Mins'] = journey_log['BT(MINUTES)']
    return airframe_data

def Add_Total_Block_Time(journey_log, airframe_data):
    airframe_data.loc[:,'TOT BLOCK Dur'] = journey_log['TOTAL BLOCK TIME']
    return airframe_data

def Add_Total_Block_Time_In_Hours(journey_log, airframe_data):#(Duration)
    airframe_data.loc[:,'TOT BLOCK Hrs'] = journey_log['TOTB(HOURS)']
    return airframe_data

def Add_Total_Block_Time_In_Minutes(journey_log, airframe_data):#(Duration)
    airframe_data.loc[:,'TOT BLOCK Mins'] = journey_log['TOTB(MINUTES)']
    return airframe_data

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
        'FLT TIME Mins': 'FH\nMins', #journey log
        'FLT TIME Dur': 'FH', #journey log
        'TAT Hrs': 'TAT\nHrs', #totals broght forward 
        'TAT Mins': 'TAT\nMins', #totals broght forward 
        'TAT Dur': 'TAT\nDur', #totals broght forward 
        'BLOCK Hrs': 'BT\nHrs', #journey log
        'BLOCK Mins': 'BT\nMins', #journey log
        'BLOCK Dur': 'BT', #journey log
        'TOT BLOCK Hrs': 'TotB\nHrs', #journey log
        'TOT BLOCK Mins': 'TotB\nMins',	#journey log
        'TOT BLOCK Dur': 'TotB' #journey log
    }