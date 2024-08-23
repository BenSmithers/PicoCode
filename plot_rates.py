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


fig, ax = plt.subplots(1,1)

#plt.errorbar(times, y=100*(data[1]-data[1][0])/data[1][0], yerr=data[2]/data[1][0], capsize=5, ecolor="k", label="Channel B", marker="d",ls='')
#plt.errorbar(times, y=100*(data[3]-data[3][0])/data[3][0], yerr=data[4]/data[3][0], capsize=5, ecolor="k", label="Channel D", marker="d",ls='')

ax.plot(times, (1-data[1])/(1-data[3]), 'bd', label="Ratio")

ax2 = plt.twinx(ax)
ax2.plot(times, 1-data[1], label="Channel B")
ax2.plot(times, 1-data[3], label="Channel D")
ax2.plot([],[], 'bd', label="Ratio")
ax2.set_ylabel("No-Pulse Rate", size=14)
ax2.set_ylim([0,1.1])
plt.legend()
ax.set_ylabel("Ratio of No-Pulse rate", size=14)
ax.set_xlabel("Time [hr]", size=14)
plt.tight_layout()
plt.savefig("./plots/stability.png", dpi=400)
plt.show()


