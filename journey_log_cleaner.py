import pandas
from file_handler import Delete_Row_From_Table


def Remove_Total_Summary_Rows(data): 
    """
    Removes rows with that contains "T0TAL -- wala -- total for the day"
    """
    return Delete_Row_From_Table(data, 'DATE', "T0TAL")


def Remove_Empty_Cycle(data):
    """
    Remove rows with CYCLE = 0.
    """
    return Delete_Row_From_Table(data, 'CYCLE', 0)

def Forward_Fill_Empty_Dates(data):
    """
    Fill in missing date in 'DATE' with last observed value(date).
    """
    data_frame = pandas.DataFrame(data)
    data_frame['DATE'] = data_frame['DATE'].replace('', pandas.NA)
    data_frame['DATE'] = data_frame['DATE'].ffill()

    return data_frame

def Convert_To_Datetime(time_stamp):
    """
    Converts time in string to datetime object.
    Args:
        time_stamp(object): time stamp in `HH:MM`
    Return:
        date time (object) conversion of time stamp
    """
    time_stamp.astype(str)
    return pandas.to_datetime(time_stamp, format = '%H:%M', errors = 'coerce')

def Compute_Duration(start_time, end_time):
    """
    Calculate the duration in seconds between two datetime objects
    Args:
        start_time: date time object to subtract
        end_time: date time onject to subtract from
    """
    block_time_duration = (end_time - start_time).dt.total_seconds()
    block_time_duration = block_time_duration.mask(block_time_duration < 0, block_time_duration + 24 * 3600) #accounts for values of the next day (00:00)

    return block_time_duration.fillna(0).astype(int) #returns 0 when value is nan

def Get_Hours_From_Duration(duration):
    """
    Get the hours component from a duration
    Args:
        duration: durations in seconds
    Return:
        hours in integers
    """
    return (duration // 3600).astype(int)


def Get_Minutes_From_Duration(duration):
    """
    Get the minutes component from a duration
    Args:
        duration: durations in seconds
    Return:
        minutes in integers
    """
    return ((duration % 3600) // 60).astype(int)


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