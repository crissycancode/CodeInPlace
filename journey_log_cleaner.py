import pandas

def Delete_Row_From_Table(data, key, value): #try to move this to a different file
    data_frame = pandas.DataFrame(data)
    data_frame = data_frame[data_frame[key] != value]

    return data_frame

def Remove_Column_From_Data(dataset, column_name):
    # #redo this
    # for row in dataset:
    #     row.pop(column_name, None)

    return Drop_Column(dataset, column_name)

def Drop_Column(dataset, column_name):
    dataset = dataset.drop(columns=[column_name], errors = 'ignore')
    return dataset

def Remove_FH_Hours_Column(data):
    return Remove_Column_From_Data(data, 'FH(HOURS)')

def Remove_FH_Minutes_Column(data):
    return Remove_Column_From_Data(data, 'FH(MINUTES)')

def Remove_BT_Hours_Column(data):
    return Remove_Column_From_Data(data, 'BT(HOURS)')

def Remove_BT_Minutes_Column(data):
    return Remove_Column_From_Data(data, 'BT(MINUTES)')

def Remove_TFH_Hours_Column(data):
    return Remove_Column_From_Data(data, 'TFH(HOURS)')

def Remove_TFH_Minutes_Column(data):
    return Remove_Column_From_Data(data, 'TFH(MINUTES)')

def Remove_TOTB_Hours_Column(data):
    return Remove_Column_From_Data(data, 'TOTB(HOURS)')

def Remove_TOTB_Minutes_Column(data):
    return Remove_Column_From_Data(data, 'TOTB(MINUTES)')




def Forward_Fill_Empty_Dates(data):
    """
    Fill in missing date in 'DATE' with last observed value(date).
    Args:
        data(list):  List of data entries
    Returns: 
        data(list): Data entries with empty 'DATE' fields filled.

    """
    data_frame = pandas.DataFrame(data)
    data_frame['DATE'] = data_frame['DATE'].replace('', pandas.NA)
    data_frame['DATE'] = data_frame['DATE'].ffill()

    return data_frame

def Delete_Row_From_Table(data, key, value): #try to move this to a different file
    data_frame = pandas.DataFrame(data)
    data_frame = data_frame[data_frame[key] != value]
    
    return data_frame

def Remove_Total_Summary_Rows(data): 
    """
    Removes rows with that contains "T0TAL -- wala -- total for the day"
    Args:
        data(list): List of data entries
    Returns:
        updated data
    """
    return Delete_Row_From_Table(data, 'DATE', "T0TAL")


def Remove_Empty_Cycle(data):
    """
    Remove rows with CYCLE = 0.
    Args:
        data(list): List of data entries
    Return:
        updated data
    """
    return Delete_Row_From_Table(data, 'CYCLE', 0)

def Compute_Duration(data, hours_col, minutes_col, duration_col):
    data_frame = pandas.DataFrame(data)
    data_frame[hours_col] = data_frame[hours_col].fillna(0).astype(int) #change from numpy to fillna for consistency with pandas ecosystem
    data_frame[hours_col] = data_frame[hours_col] * 60
    data_frame[minutes_col] = data_frame[minutes_col].replace('', '0').replace(':', '')
    data_frame[minutes_col] = data_frame[minutes_col].str.replace(':', '').astype(int)
    data_frame[duration_col] = data_frame[hours_col] + data_frame[minutes_col]

    return data_frame

def Fill_In_Flight_Hours(data):
    """
    Fillin the "FLIGHT HOURS" 
    Args:
        data (list): data entries (dictionaries).
    Returns:
        updated data with filled in flight hours
    """
    return Compute_Duration(data, 'FH(HOURS)', 'FH(MINUTES)', 'FLIGHT HOURS')
    

def Fill_In_Block_Time(data):
    """
    Fillin the "BLOCK TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'BLOCK TIME' values.
    """
    return Compute_Duration(data, 'BT(HOURS)', 'BT(MINUTES)', 'BLOCK TIME')

def Fill_In_Total_Flying_Hours(data):
    """
    Fillin the "TOTAL FLYING TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'TOTAL FLYING TIME' values.
    """
    return Compute_Duration(data, 'TFH(HOURS)', 'TFH(MINUTES)', 'TOTAL FLYING HOURS')


def Fill_In_Total_Block_Time(data):
    """
    Fillin the "TOTAL BLOCK TIME"
    Args:
        data (list): List of data entries (dictionaries).
    Returns:
        list: Data entries with standardized 'TOTAL BLOCK TIME' values.
    """
    return Compute_Duration(data, 'TOTB(HOURS)', 'TOTB(MINUTES)', 'TOTAL BLOCK TIME')
