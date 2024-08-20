import numpy as np 
import os 
import matplotlib.pyplot as plt
import time 

filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data.csv"
)

data = np.loadtxt(filename, delimiter=",").T 


print("Ran from {}hour to {}hour".format(time.localtime(data[0][0]).tm_hour, time.localtime(data[0][-1]).tm_hour))
times = (data[0] - np.min(data[0]))/3600




plt.errorbar(times, y=100*(data[1]-data[1][0])/data[1][0], yerr=data[2]/data[1][0], capsize=5, ecolor="k", label="Channel B", marker="d",ls='')
plt.errorbar(times, y=100*(data[3]-data[3][0])/data[3][0], yerr=data[4]/data[3][0], capsize=5, ecolor="k", label="Channel D", marker="d",ls='')
plt.ylabel("% Change", size=14)
plt.xlabel("Time [hr]")
plt.legend()
plt.tight_layout()
plt.savefig("./plots/stability_20hr.png", dpi=400)
plt.show()


