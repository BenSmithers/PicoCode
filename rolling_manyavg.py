import numpy as np 
import os 
import matplotlib.pyplot as plt
import time 
from scipy.interpolate import interp1d  
from scipy.optimize import minimize
from scipy import stats 
filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data_osmosis.csv"
)

data = np.loadtxt(filename, delimiter=",").T 


print("Ran from {}hour to {}hour".format(time.localtime(data[0][0]).tm_hour, time.localtime(data[0][-1]).tm_hour))
times = (data[0] - np.min(data[0]))/3600
mask = times > 160

new_err = np.sqrt(data[2]**2 + data[4]**2)

#data[3] = np.abs(np.random.randn(len(times))*0.05 +0.3)
#data[1] = np.abs(np.random.randn(len(times))*0.05 +0.6)


#plt.errorbar(times, (1-data[1])/(1-data[3]),yerr=new_err,  capsize=5, ecolor="k", marker="d",ls='')

bands = [1, 50]

fig, axes = plt.subplots(1,1, sharex=True)
axes = [axes,]
for band in bands:

    rat =  np.log(1-data[1])/np.log(1-data[3]) 
    rat =np.convolve(rat, np.ones(band),"valid")/band
    newtimes = np.convolve(times, np.ones(band), "valid")/band

    #plt.hlines(np.mean(rat[-20:]), min(times), max(times), color='k')
    axes[0].plot(newtimes, rat, label="{} msmt".format(band))
    #axes[0].set_ylabel("No-Pulse-Rate Ratio [Rolling Avg]", size=14)
    axes[0].set_ylabel(r"Ratio of $\mu$ [rolling]", size=14)

    axes[0].set_xlabel("Time [hr]")
    #plt.legend()

rat =  np.log(1-data[1])/np.log(1-data[3]) 

band =50 
newtimes = np.convolve(times, np.ones(band), "valid")/band
newrat =np.convolve(rat, np.ones(band),"valid")/band

interpo = interp1d(newtimes, newrat, bounds_error= False)


error = interpo(times) - rat

error = np.percentile(np.abs(error[np.logical_and(np.logical_not(np.isnan(error)), times>80)]), 68)


#axes[1].plot(times, error)
#axes[1].set_ylabel("Residuals")
axes[0].set_xlim([150,240])
#axes[1].set_ylim([-0.3, 0.3])
axes[0].set_ylim([0.2,0.4])
axes[0].set_ylim([0,10])
def func_eval(xs, params):
    return params[0]*xs + params[1] 

def metric(params, nosum=False):
    # params are m and b 
    # returns a LLH

    y = func_eval(times[mask], params)
    if nosum:
        return  0.5*((rat[mask] - y)/0.03)**2
    else:
        return np.sum( 0.5*((rat[mask] - y)/error)**2 )

x0 = [0.01, np.mean(rat)]
bounds = [[-5, 5], [0, 1000]]
res = minimize(metric, x0=x0, bounds=bounds, options={"eps":1e-20, "ftol":1e-20, "gtol":1e-20})
fit_min = res.x
jav = res.jac 
print(jav)
axes[0].plot(times, func_eval(times, fit_min), label="Fit", color='k',alpha=0.2, zorder=-5)

axes[0].legend()

all_norms = np.linspace(0.2, 0.4, 100)
all_slopes=np.linspace(-0.1,0.1, 100)

meshslope, meshnorm = np.meshgrid(all_slopes, all_norms)

dof = len(times)-2
print( 1 - stats.chi2.cdf(metric(fit_min), dof))


plt.savefig("./plots/rolling.png", dpi=400)
plt.show()


