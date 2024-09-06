import pandas as pd 
import pytz
from datetime import datetime 
from datetime import timezone
import time 
import numpy as np 

def load_from(start, end):
    
    """
    returns pressure data from the UTC period starting from `start` to `end`
    """

    local = pytz.timezone("America/Los_Angeles")
    temmplate = "./weather/en_climate_hourly_BC_1108824_{:02d}-{}_P1H.csv"

    start_obj = datetime.fromtimestamp(start)
    end_obj = datetime.fromtimestamp(end)

    times = []
    pressures = []
    temperatures = []

    year = start_obj.year
    month = start_obj.month 

    while year<=end_obj.year and month<=end_obj.month:
        # load next file 
        data = pd.read_csv(temmplate.format(month, year))    
        time_col = data["Date/Time (LST)"][:]
        for entry in time_col:
            simpletime = datetime.strptime(entry, '%Y-%m-%d %H:%M')
            local_dt = local.localize(simpletime, is_dst=None)
            times.append(
                time.mktime(local_dt.astimezone(pytz.utc).timetuple())
            )
        pressures += np.array(data["Stn Press (kPa)"]).tolist()
        temperatures +=  np.array(data["Temp (°C)"]).tolist()

        month+=1
        if month==13:
            year +=1 
            month = 1
            
    times = np.array(times)
    
    pressures=  np.array(pressures)
    temperatures = np.array(temperatures)

    mask = np.logical_and(times>start, times<end)
    return times[mask], temperatures[mask], pressures[mask]


