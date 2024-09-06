import json 

import numpy as np
import matplotlib.pyplot as plt 


_obj = open("charge_distrib_log.json",'rt')
data = json.load(_obj)
_obj.close()

print(len(data))

if False:
    for entry in data[30:35]:
        plt.stairs(entry["monitor"]/np.sum(entry["monitor"]), entry["bins"], color="blue",alpha=0.5, ls='-')
        plt.stairs(entry["receiver"]/np.sum(entry["receiver"]), entry["bins"], color="orange",alpha=0.5, ls='-')


    for entry in data[150:155]:
        plt.stairs(entry["monitor"]/np.sum(entry["monitor"]), entry["bins"], color="red",alpha=0.5)
        plt.stairs(entry["receiver"]/np.sum(entry["receiver"]), entry["bins"], color="purple",alpha=0.5)


entry = data[-1]
plt.stairs(entry["monitor"]/np.sum(entry["monitor"]), entry["bins"], color="green",alpha=0.5)
plt.stairs(entry["receiver"]/np.sum(entry["receiver"]), entry["bins"], color="yellow",alpha=0.5)

if False:
    plt.plot([], [], marker="", ls="-", color="blue",label="monitor")
    plt.plot([], [], marker="", ls="-", color="red",label="monitor-middle")
    plt.plot([], [], marker="", ls="-", color="green",label="monitor-latest")
    plt.plot([], [], marker="", ls="-", color="orange",label="receiver")


    plt.plot([], [], marker="", ls="-", color="purple",label="receiver-middle")


    plt.plot([], [], marker="", ls="-", color="yellow",label="receiver-latest")
plt.yscale('log')
plt.xlabel("Amplitude [mV]", size=14)
plt.ylabel("Normalized Counts",size=14)
plt.legend()
plt.savefig("./plots/charge_distribs.png", dpi=400)
plt.show()