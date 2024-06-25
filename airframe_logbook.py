from time_utils import (Convert_To_Datetime)

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
        'TAT': 'last',
        'FLT TIME Dur': 'last',
        'BLOCK Dur': 'last',
        'TOT BLOCK Dur': 'last'
    }).reset_index()

    # sort by 'DATE'
    aggregated_data = aggregated_data.sort_values(by = 'DATE')
    # format to day-month-year
    aggregated_data['DATE'] = aggregated_data['DATE'].dt.strftime('%d-%b-%y')

    return aggregated_data


def Copy_Date_From_JourneyLog(journey_log, airframe_log): #step 1 copy date from JL
    journey_log_columns = ['DATE']
    Validate_Columns(journey_log_columns, journey_log, 'journey_log')
    airframe_log_columns = ['DATE']
    Validate_Columns(airframe_log_columns, airframe_log, 'airframe_log')

    airframe_log = journey_log[['DATE']].copy()
    airframe_log.loc[:, 'DATE'] = airframe_log['DATE']

    return airframe_log


def Copy_Cycles_From_JourneyLog(journey_log, airframe_log):
    airframe_log.loc[:, 'CYCLE'] = journey_log['CYCLE']
    return airframe_log


def Get_Total_Accumulated_Cycle(airframe_log, totals_brought_forward):
    #(TAC) for an aircraft or engine refers to the cumulative count of flight cycles since the component was first put into service.
    #This means 'Flight Brought Forward' is now needed along with Journey Log
    #Total_accumulated_cycle = total_accumulated_cycle + current_cycles
    tac = totals_brought_forward['TAC AF'][0]
    cycle = airframe_log['CYCLE'].cumsum()
    airframe_log['TAC'] = tac + cycle
    return airframe_log


def Get_Total_Airframe_Time(journey_log, airframe_log, totals_brought_forward): #(Duration)

    tat_hours = totals_brought_forward['TAT AF Hrs'][0] * 60
    tat_minutes = totals_brought_forward['TAT AF Mins'][0]
    tat  = tat_hours + tat_minutes
    flight_hours = journey_log['FLIGHT HOURS'].cumsum()

    airframe_log['TAT'] = tat + flight_hours
    airframe_log['TAT'] = airframe_log['TAT'].astype(int)
    return airframe_log

def Get_Flight_Time(journey_log, airframe_log):#(Duration)
    #Flight Time is same as Flight Hours (FH) in Journey Log
    airframe_log['FLT TIME Dur'] = journey_log['FLIGHT HOURS']
    return airframe_log

def Get_Block_Time(journey_log, airframe_log):#(Duration)
    airframe_log['BLOCK Dur'] = journey_log['BLOCK TIME']
    return airframe_log

def Get_Total_Block_Time(journey_log, airframe_log):#(Duration)
    airframe_log['TOT BLOCK Dur'] = journey_log['TOTAL BLOCK TIME']
    return airframe_log


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
        'TOT BLOCK hrs': 'TotB\nHrs', #journey log
        'TOT BLOCK Mins': 'TotB\nMins',	#journey log
        'TOT BLOCK Dur': 'TotB' #journey log
    }