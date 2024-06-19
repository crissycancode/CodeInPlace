import pandas
from file_handler import Delete_Row_From_Table
from time_utils import (Forward_Fill_Empty_Dates,
                        Convert_To_Datetime,
                        Compute_Duration,
                        Get_Hours_From_Duration,
                        Get_Minutes_From_Duration)


def Remove_Total_Summary_Rows(data): 
    """
    Removes rows with that contains "T0TAL -- wala -- total for the day"
    Args:
        data : flight data that represents flight log entry.
    Return:
        data frame without the deleted row
    """
    return Delete_Row_From_Table(data, 'DATE', "T0TAL")


def Remove_Empty_Cycle(data):
    """
    Removes rows cycles that have 0 value
    Args:
        data : flight data that represents flight log entry.
    Return:
        data frame without the deleted row
    """
    return Delete_Row_From_Table(data, 'CYCLE', 0)

def Update_Empty_Flight_Dates(data):
    """
    Fill in missing date with last observed value(date).
    Args:
        data : flight data that represents flight log entry.
    Return:
        data frame with updated dates
    """
    return Forward_Fill_Empty_Dates(data,'DATE')


def Update_Flight_Hours(data):
    """
    Uses the flight data to compute the flight duration, flight hours/minutes, and total cumulative flight hours.
    Args:
        data : flight data that represents flight log entry.
    Return:
        data frame with the following columns updated:
            'FH(HOURS)' : int
                The hours part of the flight duration.
            'FH(MINUTES)' : int
                The minutes part of the flight duration.
            'FLIGHT HOURS' : float
                The total flight duration in seconds.
            'TFH(HOURS)' : int
                The cumulative sum of flight hours.
            'TFH(MINUTES)' : int
                The cumulative sum of flight minutes.
            'TOTAL FLYING HOURS' : float
                The cumulative sum of flight durations in seconds.
    """
        
    data_frame = pandas.DataFrame(data)
    take_off = Convert_To_Datetime(data_frame['TAKE OFF'])
    on_ground = Convert_To_Datetime(data_frame['ON GROUND'])

    duration = Compute_Duration(take_off, on_ground)

    #get the hours and minutes
    hours = Get_Hours_From_Duration(duration)
    minutes = Get_Minutes_From_Duration(duration)

    #assigned values to columns
    data_frame['FH(HOURS)'] = hours
    data_frame['FH(MINUTES)'] = minutes
    data_frame['FLIGHT HOURS'] = duration
    data_frame['TFH(HOURS)'] = data_frame['FH(HOURS)'].cumsum()
    data_frame['TFH(MINUTES)'] = data_frame['FH(MINUTES)'].cumsum()
    data_frame['TOTAL FLYING HOURS'] = data_frame['FLIGHT HOURS'].cumsum()
    return data_frame


def Update_Block_Time(data):
    """
    Uses the flight data to compute the block time duration, block time in hours/minutes, and total cumulative block time.
    Args:
        data : flight data that represents flight log entry.
    Return:
        data frame with the following columns updated:
            'BT(HOURS)' : int
                The hours part of the block time duration.
            'BT(MINUTES)' : int
                The minutes part of the block time duration.
            'BLOCK TIME' : float
                The total block time duration in seconds.
            'TOTB(HOURS)' : int
                The cumulative sum of block time hours.
            'TOTB(MINUTES)' : int
                The cumulative sum of block time minutes.
            'TOTAL BLOCK TIME' : float
                The cumulative sum of block time durations in seconds.
    """
    data_frame = pandas.DataFrame(data)
 
    off_blocks = Convert_To_Datetime(data_frame['OFF BLOCKS'])
    on_blocks = Convert_To_Datetime(data_frame['ON BLOCKS'])

    duration = Compute_Duration(off_blocks, on_blocks)

    #get the hours and minutes
    hours = Get_Hours_From_Duration(duration)
    minutes = Get_Minutes_From_Duration(duration)

    #assigned values to columns
    data_frame['BT(HOURS)'] = hours
    data_frame['BT(MINUTES)'] = minutes
    data_frame['BLOCK TIME'] = duration
    data_frame['TOTB(HOURS)'] = data_frame['BT(HOURS)'].cumsum()
    data_frame['TOTB(MINUTES)'] = data_frame['BT(MINUTES)'].cumsum()
    data_frame['TOTAL BLOCK TIME'] = data_frame['BLOCK TIME'].cumsum()

    return data_frame

def Update_Total_Cycle(data):
    """
    Uses the flight data to compute cumulative cycle.
    Args:
        data : flight data that represents flight log entry.
    Return:
        cumulative sum of flight cycles
    """
    data_frame = pandas.DataFrame(data)
    data_frame['TOTAL CYCLE'] = data_frame['CYCLE'].cumsum()

    return data_frame

def Journey_Log_Headers():
    """
    Heads to display
    return: dictionary of custom headers
    """
    return {
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