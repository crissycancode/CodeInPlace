
def Backfill_Empty_Dates(data):
    """
    Fill in missing date in 'DATE' with preceding (previous) values.
    Args:
        data(list):  List of data entries
    Returns: 
        data(list): Data entries with empty 'DATE' fields filled.
    """
    last_non_empty_date = None

    for data_entry in data:
        date_value = data_entry.get("DATE")
        
        if not date_value:
            if last_non_empty_date:
                data_entry["DATE"] = last_non_empty_date
        else:
            last_non_empty_date = date_value
    
    return data


def Remove_Total_Summary_Rows(data): 
    """
    Removes rows that summarize the totals for the day.
    Args:
        data(list): List of data entries
    Returns:
        updated_data: Data entires with total summary rows removed.
    """
    updated_data = [data_entry for data_entry in data if data_entry.get("DATE") != "T0TAL"]
    return updated_data


def Remove_Empty_Flight_Hours(data):
    """
    Remove rows with FLIGHT_HOURS that has empty value.
    Args:
        data(list): List of data entries
    Return:
        updated_data: Data entied with empty values FLIGHT HOURS removed.
    """
    updated_data = [data_entry for data_entry in data if data_entry.get("FLIGHT HOURS") != "0"]
    return updated_data


def Fill_In_Flight_Hours(data):
    """
    Fillin the "FILIGHT HOURS"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'FILIGHT HOURS' values.
    """
    for data_entry in data:
        fh_hours = data_entry.get("FH(HOURS)", "").strip()
        fh_minutes = data_entry.get("FH(MINUTES)", "").strip().replace(":", "")

        flight_hours = int(fh_hours) if fh_hours.isdigit() else 0
        flight_minutes = int(fh_minutes) if fh_minutes.isdigit() else 0
        flight_hours = (flight_hours * 60) + flight_minutes

        data_entry["FLIGHT HOURS"] = str(flight_hours) #this needs to be displayed as "1:08 (1H 08MIN)" create a function that will style it this way but not save
    return data

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
