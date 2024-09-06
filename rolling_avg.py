import numpy as np 
import os 
import matplotlib.pyplot as plt
import time 
from scipy.optimize import minimize

filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data_osmosis.csv"
)

data = np.loadtxt(filename, delimiter=",").T 


print("Ran from {}hour to {}hour".format(time.localtime(data[0][0]).tm_hour, time.localtime(data[0][-1]).tm_hour))
times = (data[0] - np.min(data[0]))/3600


new_err = np.sqrt(data[2]**2 + data[4]**2)


band = 50

rat =  np.log(1-data[1])/np.log(1-data[3]) 
rat =np.convolve(rat, np.ones(band),"valid")/band
newtimes = np.convolve(times, np.ones(band), "valid")/band

mask = newtimes > 200
newtimes = newtimes[mask]
rat=rat[mask]

def func_eval(xs, params):
    return params[0]*newtimes + params[1] 

def metric(params):
    # params are m and b 

    y = func_eval(newtimes, params)
    return np.sum( (rat - y)**2 )

x0 = [0.01, np.mean(rat)]
bounds = [[-5, 5], [0, 1000]]
res = minimize(metric, x0=x0, bounds=bounds, options={"eps":1e-20, "ftol":1e-20, "gtol":1e-20})
fit_min = res.x
jav = res.jac 


print(res)
fix, ax = plt.subplots(1,1)

ax2 = ax.twinx()
ax2.plot(newtimes, 100*(func_eval(newtimes, fit_min)-rat)/rat , label="Deviation from linear", color="gray", alpha=0.4)
#plt.hlines(np.mean(rat[-20:]), min(times), max(times), color='k')
ax.plot(newtimes, rat, label="Rolling Avg".format(band))
ax.plot(newtimes, func_eval(newtimes, fit_min), label="Fit")
ax.set_ylabel("No-Pulse-Rate Ratio [Rolling Avg]", size=14)
ax.plot([],[], label="% Devaition", color="gray", alpha=0.4)
ax.set_ylabel(r"Ratio of $\mu=log(1-P_{0})$ [Rolling]", size=14)

ax.set_xlabel("Time [hr]")
#plt.legend()
plt.tight_layout()
ax.set_xlim([200,265])
ax.set_ylim([3.5,4])
#ax2.set_ylim([-10,10])
ax.legend()


plt.savefig("./plots/rolling.png", dpi=400)
plt.show()


