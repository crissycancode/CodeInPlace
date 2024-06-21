import pandas
import logging

def Forward_Fill_Empty_Dates(data, key):
    """
    Fill in missing date with last observed value(date).
    Args:
        data : data that represents table entry.
        key : the column name which contains the dates.
    Return:
        data frame with updated dates
    """
    data_frame = pandas.DataFrame(data)
    data_frame[key] = data_frame[key].replace('', pandas.NA)
    data_frame[key] = Format_Date(data_frame[key])
    data_frame[key] = data_frame[key].ffill()

    return data_frame

def Format_Date(date):
    """
    Format the date series to replace spaces and periods with hyphens.
    Args:
        date: dates as string
    Return:
        formatted dates
    """
    return date.str.replace(' ', '-', regex = False).str.replace('.', '-', regex = False)

def Convert_To_Datetime_In_Hrs_Mins(time_stamp):
    """
    Converts time in string to datetime object
    Args:
        time_stamp(object): time stamp in `HH:MM`
    Return:
        date time (object) conversion of time stamp
    """
    # if not isinstance(time_stamp, str):
    #     time_stamp = time_stamp.astype(str)
    # return pandas.to_datetime(time_stamp, format = '%H:%M', errors = 'coerce')

    try:
        return pandas.to_datetime(time_stamp, format = '%H:%M', errors='coerce')
    except Exception as e:
        logging.error(f"Error parsing datetime: {e}")
        return pandas.NaT  # Return NaT for failed parses

def Convert_To_Datetime(time_stamp):
    """
    Converts time in string to datetime object
    Args:
        time_stamp(object): time stamp in `HH:MM`
    Return:
        date time (object) conversion of time stamp
    """
    try:
        return pandas.to_datetime(time_stamp, format = '%d-%b-%y', errors='coerce')
    except Exception as e:
        logging.error(f"Error parsing datetime: {e}")
        return pandas.NaT  # Return NaT for failed parses


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