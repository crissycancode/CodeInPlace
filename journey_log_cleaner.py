import pandas
from file_handler import Convert_To_CSV

def Delete_Row_From_Table(data, key, value): 
    data_frame = pandas.DataFrame(data)
    data_frame = data_frame[data_frame[key] != value]
    return data_frame


def Forward_Fill_Empty_Dates(data):
    """
    Fill in missing date in 'DATE' with last observed value(date).
    """
    data_frame = pandas.DataFrame(data)
    data_frame['DATE'] = data_frame['DATE'].replace('', pandas.NA)
    data_frame['DATE'] = data_frame['DATE'].ffill()

    return data_frame


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

def Flight_Hours_In_Hours(data):
    data_frame = pandas.DataFrame(data)

    take_off_str  = data_frame['TAKE OFF'].astype(str)
    take_off_date = pandas.to_datetime(take_off_str, format = '%H:%M', errors = 'coerce')

    #new on ground value
    on_ground_str  = data_frame['ON GROUND'].astype(str)
    on_ground_date = pandas.to_datetime(on_ground_str, format = '%H:%M', errors = 'coerce')

    #calculate flight duration
    flight_duration = (on_ground_date - take_off_date).dt.total_seconds()
    flight_duration = flight_duration.mask(flight_duration < 0, flight_duration + 24 * 3600)

    #get the hours and minutes
    hours = (flight_duration // 3600).astype(int)
    minutes = ((flight_duration % 3600) // 60).astype(int)

    #assigned values to columns
    data_frame['FH(HOURS)'] = hours
    data_frame['FH(MINUTES)'] = minutes
    data_frame['FLIGHT HOURS'] = flight_duration
    data_frame['TFH(HOURS)'] = data_frame['FH(HOURS)'].cumsum()
    data_frame['TFH(MINUTES)'] = data_frame['FH(MINUTES)'].cumsum()
    data_frame['TOTAL FLYING HOURS'] = data_frame['FLIGHT HOURS'].cumsum()
    return data_frame


def Flight_Hours_In_Minutes(data):
    pass

def Fill_In_Flight_Hours(data):
    pass
    
def Fill_In_Total_Flying_Hours(data):
    pass

def Fill_In_Block_Time(data):
    """
    Fillin the "BLOCK TIME"
    """
    pass




def Fill_In_Total_Block_Time(data):
    """
    Fillin the "TOTAL BLOCK TIME"
    """
    pass



def Block_Values(data):
    data_frame = pandas.DataFrame(data)
    # on blocks - off blocks

    off_blocks_str  = data_frame['OFF BLOCKS'].astype(str)
    off_blocks_date = pandas.to_datetime(off_blocks_str, format = '%H:%M', errors = 'coerce')

    #new on ground value
    on_blocks_str  = data_frame['ON BLOCKS'].astype(str)
    on_blocks_date = pandas.to_datetime(on_blocks_str, format = '%H:%M', errors = 'coerce')

    #calculate flight duration
    block_time_duration = (on_blocks_date - off_blocks_date).dt.total_seconds()
    block_time_duration = block_time_duration.mask(block_time_duration < 0, block_time_duration + 24 * 3600)

    block_time_duration_filled = block_time_duration.fillna(0)

    #get the hours and minutes
    hours = (block_time_duration_filled // 3600).astype(int)
    minutes = ((block_time_duration_filled % 3600) // 60).astype(int)

    #assigned values to columns
    data_frame['BT(HOURS)'] = hours
    data_frame['BT(MINUTES)'] = minutes
    data_frame['BLOCK TIME'] = block_time_duration
    data_frame['TOTB(HOURS)'] = data_frame['BT(HOURS)'].cumsum()
    data_frame['TOTB(MINUTES)'] = data_frame['BT(MINUTES)'].cumsum()
    data_frame['TOTAL BLOCK TIME'] = data_frame['BLOCK TIME'].cumsum()

    return data_frame

def Total_Cycle(data):
    data_frame = pandas.DataFrame(data)
    data_frame['TOTAL CYCLE'] = data_frame['CYCLE'].cumsum()

    return data_frame