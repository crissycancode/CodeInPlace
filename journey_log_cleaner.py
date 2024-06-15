import pandas
import numpy

def Delete_Row_From_Table(data, key, value): #try to move this to a different file
    data_frame = pandas.DataFrame(data)
    data_frame = data_frame[data_frame[key] != value]
    updated_data = data_frame.to_dict(orient='records')

    return updated_data


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


def Remove_Total_Summary_Rows(data): 
    """
    Removes rows with that contains "T0TAL -- wala -- total for the day"
    Args:
        data(list): List of data entries
    Returns:
        updated data
    """
    return Delete_Row_From_Table(data, 'DATE', "T0TAL")


def Remove_Empty_Flight_Hours(data):
    """
    Remove rows with FLIGHT HOURS that has 0 value.
    Args:
        data(list): List of data entries
    Return:
        updated data
    """
    return Delete_Row_From_Table(data, 'FLIGHT HOURS', "0")

def Compute_Duration_In_Minutes(hours, minutes):
    # see if this is still needed to break down function for duration
    pass
    return 

def Fill_In_Flight_Hours(data):
    """
    Fillin the "FLIGHT HOURS" 
    Args:
        data (list): data entries (dictionaries).
    Returns:
        updated data with filled in flight hours
    """
    #same for fillin_block_time, total flying hours, total block time
    data_frame = pandas.DataFrame(data)

    #note: convert the columns to int before looping

    data_frame['FH(HOURS)'] = numpy.nan_to_num(data_frame['FH(HOURS)'], nan=0).astype(int) #converts float64 to int

    for i in range (len(data_frame['FH(HOURS)'])):

        data_frame.at[i,'FH(HOURS)'] = data_frame['FH(HOURS)'][i] * 60 #converts hours to minutes
        data_frame.at[i,'FH(MINUTES)'] = int(data_frame['FH(MINUTES)'][i][1:]) #converts the string to in after removing ':'
        data_frame.at[i,'FLIGHT HOURS'] = data_frame.at[i,'FH(HOURS)'] + data_frame.at[i,'FH(MINUTES)']#compute for Flight Hours
    
    data_frame['FLIGHT HOURS'] = data_frame['FLIGHT HOURS'].astype(int) #converts float64 to int
    
    print(f"{data_frame['FH(HOURS)']}")

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
