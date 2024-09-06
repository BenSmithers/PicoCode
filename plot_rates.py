import numpy as np 
import os 
import matplotlib.pyplot as plt
import time 
import datetime 

from temperature import load_from

filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data_osmosis.csv"
)


logfile = open("log.txt",'rt')


processed = []
for line in logfile.readlines():
    split = line.split("-")
    times = float(split[0])
    note = "-".join(split[1:])
    note = note.replace("\n", "")
    processed.append([times, note])  
logfile.close()

data = np.loadtxt(filename, delimiter=",").T 


print("Ran from {}hour to {}hour".format(time.localtime(data[0][0]).tm_hour, time.localtime(data[0][-1]).tm_hour))
times = (data[0] - np.min(data[0]))/3600



fig, axes = plt.subplots(2,1, sharex=True)

#plt.errorbar(times, y=100*(data[1]-data[1][0])/data[1][0], yerr=data[2]/data[1][0], capsize=5, ecolor="k", label="Channel B", marker="d",ls='')
#plt.errorbar(times, y=100*(data[3]-data[3][0])/data[3][0], yerr=data[4]/data[3][0], capsize=5, ecolor="k", label="Channel D", marker="d",ls='')

for entry in processed:
    thistime = (entry[0]- np.min(data[0]))/3600
    if thistime>min(times) and thistime<max(times):
        print(thistime, entry[1])

axes[0].plot(times, np.log(1-data[1])/np.log(1-data[3]), color='gray', marker='d', label="Ratio")
axes[0].set_ylim([3,7])
axes[0].set_xlim([75, 265])
ax2 = plt.twinx(axes[0])
ax2.plot(times, -np.log(1-data[1]), label="Channel B")
ax2.plot(times, -np.log(1-data[3]), label="Channel D")
ax2.plot([],[], 'bd', label="Ratio")
ax2.set_ylabel(r"$\mu=log(1-P_{0})$", size=14)
ax2.set_ylim([0,2])
plt.legend(loc='upper left')
axes[0].set_ylabel(r"Ratio of $\mu=-log(1-P_{0})$", size=14)
#axes[0].set_ylabel("Ratio no-pulse-rates", size=14)
axes[1].set_xlabel("Time [hr]", size=14)

newtimes, temps, pres = load_from(data[0][0], data[0][-1])
newtimes = (newtimes - np.min(data[0]))/3600
temps = temps + 273.15

if True:
    axes[1].plot(newtimes, 100*(temps-temps[0])/(temps[0]), color="red", label=r"$\Delta$Temperature [K]")
    #axes[1].plot([],[], color="blue", label="Pressure")
    axes[1].set_ylabel(r"% Diff")
    axes[1].plot(newtimes, 100*(pres-pres[0])/pres[0], color="blue", label=r"$\Delta$Pressure [kPa]")
    axes[1].plot([], [], color="green", label="Bubble")
    axes[1].legend(loc="lower right")
    
    ttwax = axes[1].twinx()
    cool_ratio = ((temps)/pres)*(pres[0]/(temps[0]))
    ttwax.plot(newtimes, cool_ratio, color="green", label="Bubble")
    ttwax.set_ylabel("Bubble Volume")

plt.tight_layout()
plt.savefig("./plots/stability_mu.png", dpi=400)
plt.show()



