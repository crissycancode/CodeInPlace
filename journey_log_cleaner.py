
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


def Standardize_Operation_Type(data):
    """
    Standardize 'OPERATION_TYPE' values to 'NIGHT' if they are 'N'.
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'OPERATION_TYPE' values.
    """
    for data_entry in data:
        if "OPERATION" in data_entry:
            if data_entry["OPERATION"] in ("N"):
                data_entry["OPERATION"] = "NIGHT"
            else:
                data_entry["OPERATION"] = "-"
    return data

def Fillin_Flight_Hours(data):
    """
    Fillin the "FILIGHT HOURS"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'FILIGHT HOURS' values.
    """
    for data_entry in data:

        flight_hours = int(data_entry["FH(HOURS)"]) * 60
        flight_minutes = int(data_entry["FH(MINUTES)"].replace(":", ""))
        data_entry["FLIGHT HOURS"] = str(flight_hours + flight_minutes)
        #this needs to be displayed as "1:08 (1H 08MIN)" create a function that will style it this way but not save
    return data

