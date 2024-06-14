import pandas


def Backfill_Empty_Dates(data):
    """
    Fill in missing date in 'DATE' with preceding (previous) values.
    Args:
        data(list):  List of data entries
    Returns: 
        data(list): Data entries with empty 'DATE' fields filled.
    """
    data_frame = pandas.DataFrame(data)
    data_frame['DATE'] = data_frame['DATE'].replace('', pandas.NA)
    data_frame['DATE'] = data_frame['DATE'].ffill()
    data = data_frame.to_dict(orient='records')

    return data


def Remove_Row_From_Table(data, key, value): #try to put this to a different file
    data_frame = pandas.DataFrame(data)
    data_frame = data_frame[data_frame[key] != value]
    updated_data = data_frame.to_dict(orient='records')

    return updated_data


def Remove_Total_Summary_Rows(data): 
    """
    Removes rows with that contains "T0TAL -- wala -- total for the day"
    Args:
        data(list): List of data entries
    Returns:
        updated data
    """
    return Remove_Row_From_Table(data, 'DATE', "T0TAL")


def Remove_Empty_Flight_Hours(data):
    """
    Remove rows with FLIGHT HOURS that has 0 value.
    Args:
        data(list): List of data entries
    Return:
        updated data
    """
    return Remove_Row_From_Table(data, 'FLIGHT HOURS', "0")


def Fill_In_Flight_Hours(data):
    """
    Fillin the "FILIGHT HOURS"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        updated data with filled in flight hours
    """
    
    data_frame = pandas.DataFrame(data)

    #convert from hours to minutes, replace empty cells with '0' to make sure there is no null value, cast to interger
    data_frame['FH(HOURS)'] = data_frame['FH(HOURS)'].str.strip().replace('', '0').astype(int) 
    #remove ':', replace empty cells with '0' to make sure there is no null value, cast to interger
    data_frame['FH(MINUTES)'] = data_frame['FH(MINUTES)'].str.strip().str.replace(':', '').replace('', '0').astype(int)

    #compute the fliying hours in minutes
    data_frame['FLIGHT HOURS'] = (data_frame['FH(HOURS)'] * 60 + data_frame['FH(MINUTES)']).astype(str)

    updated_data = data_frame.to_dict(orient='records')

    return updated_data
    

def Fill_In_Block_Time(data):
    """
    Fillin the "BLOCK TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'BLOCK TIME' values.
    """
    for data_entry in data:
        hours = data_entry.get("BT(HOURS)", "").strip()
        minutes = data_entry.get("BT(MINUTES)", "").strip().replace(":", "")

        block_time_in_hours = int(hours) if hours.isdigit() else 0
        block_time_in_minutes = int(minutes) if minutes.isdigit() else 0
        block_time = (block_time_in_hours * 60) + block_time_in_minutes

        data_entry["BLOCK TIME"] = str(block_time)
        #this needs to be displayed as "1:08 (1H 08MIN)" create a function that will style it this way but not save

    return data

def Fill_In_Total_Flying_Hours(data):
    """
    Fillin the "TOTAL FLYING TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'TOTAL FLYING TIME' values.
    """
    for data_entry in data:
        hours = data_entry.get("TFH(HOURS)", "").strip()
        minutes = data_entry.get("TFH(MINUTES)", "").strip().replace(":", "")

        total_flying_time_in_hours = int(hours) if hours.isdigit() else 0
        total_flying_time_in_minutes = int(minutes) if minutes.isdigit() else 0
        total_flying_time = (total_flying_time_in_hours * 60) + total_flying_time_in_minutes

        data_entry["TOTAL FLYING HOURS"] = str(total_flying_time)
        #this needs to be displayed as "1:08 (1H 08MIN)" create a function that will style it this way but not save
    return data


def Fill_In_Total_Block_Time(data):
    """
    Fillin the "TOTAL BLOCK TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'TOTAL BLOCK TIME' values.
    """
    for data_entry in data:
        hours = data_entry.get("TOTB(HOURS)", "").strip()
        minutes = data_entry.get("TOTB(MINUTES)", "").strip().replace(":", "")

        total_flying_time_in_hours = int(hours) if hours.isdigit() else 0
        total_flying_time_in_minutes = int(minutes) if minutes.isdigit() else 0
        total_flying_time = (total_flying_time_in_hours * 60) + total_flying_time_in_minutes

        data_entry["TOTAL BLOCK TIME"] = str(total_flying_time)
        #this needs to be displayed as "1:08 (1H 08MIN)" create a function that will style it this way but not save
    return data
