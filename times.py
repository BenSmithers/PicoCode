from time import time 
begin = time()

from utils import Scope, MAXSAMPLES, ReturnType
from picosdk.ps3000a import ps3000a as ps

import matplotlib.pyplot as plt 
import numpy as np
import os 

#with Scope() as scope_obj:

import sys 
if MAXSAMPLES!= 25000:
    print("Max samples changed - change the number of expected pulses")


scope_obj = Scope()
scope_obj.__enter__()
print(scope_obj)

scope_obj.enable_channel(0, collect = True)
#scope_obj.set_trigger(0)

scope_obj.enable_channel(1, pulse_threshold=5)
scope_obj.enable_channel(3, pulse_threshold=5)

bins = np.linspace(0,400, 100)

data = np.zeros(len(bins)-1)
data2 = np.zeros(len(data))

panet = []
pbnet = []
pcnet = []



filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data.csv"
)

while True:
    pa = 2661

    start = time()
    pa, pb, pc =  scope_obj.sample(ReturnType.Amplitudes)
    end = time()

    data += np.histogram(pb, bins)[0]
    data2+=np.histogram(pc, bins)[0]



        
    #plt.plot(range(len(pa)), pa, label="max")
    #plt.plot(range(len(pb)), pb, label="min")
    #plt.show()
    if (time() - begin)/60 > 1.:
        break
plt.stairs(data, bins, label="Channel B")
plt.stairs(data2, bins, label="Channel D")
plt.legend()
plt.xlabel("mV Signal", size=14)
plt.ylabel("Counts", size=14)
plt.yscale('log')
plt.savefig("./plots/amp_distribution.png",dpi=400)
plt.show()
