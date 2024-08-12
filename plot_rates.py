import numpy as np 
import os 
import matplotlib.pyplot as plt 


filename = os.path.join(
    os.path.dirname(__file__),
    "data.csv"
)

data = np.loadtxt(filename, delimiter=",").T 

times = (data[0] - np.min(data[0]))/60

plt.errorbar(times, y=100*(data[1]-data[1][0])/data[1][0], yerr=data[2]/data[1][0], capsize=5, ecolor="k", label="Channel A", marker="d")
plt.errorbar(times, y=100*(data[3]-data[3][0])/data[3][0], yerr=data[4]/data[3][0], capsize=5, ecolor="k", label="Channel B", marker="d")
plt.ylabel("% Change", size=14)
plt.xlabel("Time [min]")
plt.legend()
plt.show()


