"""
    Short example script showing how the weather data are accessed 
"""

from temperature import load_from
import time
import datetime 
import numpy as np
start = datetime.date(year=2024, month=8, day= 28)
end =  datetime.date(year=2024, month=9, day= 5)

start = time.mktime(start.timetuple())
end = time.mktime(end.timetuple())

times, temps, pres = load_from(start, end)
print(len(times))
import matplotlib.pyplot as plt 

times = (times -np.min(times))/3600
fig, ax = plt.subplots(1,1)
ax.plot(times, temps, color="red", label="Temperature")
ax.set_xlabel("Time H")
ax.set_ylabel("Temps [C]")
ax2 = ax.twinx()
ax2.plot(times, pres, color="blue", label="Pressure")
ax2.set_ylabel("Pres")
plt.legend()
plt.show()