import numpy as np 
import os 
import matplotlib.pyplot as plt
import time 

filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data_new.csv"
)

data = np.loadtxt(filename, delimiter=",").T 


print("Ran from {}hour to {}hour".format(time.localtime(data[0][0]).tm_hour, time.localtime(data[0][-1]).tm_hour))
times = (data[0] - np.min(data[0]))/3600


new_err = np.sqrt(data[2]**2 + data[4]**2)

#plt.errorbar(times, (1-data[1])/(1-data[3]),yerr=new_err,  capsize=5, ecolor="k", marker="d",ls='')

rat =  (1-data[1])/(1-data[3]) 
rat =np.convolve(rat, np.ones(5),"valid")/5
times = np.convolve(times, np.ones(5), "valid")/5

plt.hlines(np.mean(rat[-20:]), min(times), max(times), color='k')
plt.plot(times, rat)
plt.ylabel("No-Pulse-Rate Ratio [Rolling Avg]", size=14)
plt.xlabel("Time [hr]")
#plt.legend()
plt.tight_layout()
plt.savefig("./plots/rolling.png", dpi=400)
plt.show()


