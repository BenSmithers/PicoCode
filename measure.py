from time import time 
begin = time()

from utils import Scope, MAXSAMPLES
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

scope_obj.enable_channel(1, pulse_threshold=38)
scope_obj.enable_channel(3, pulse_threshold=14)

bins = np.linspace(0,400, 100)

data = np.zeros(len(bins)-1)
data2 = np.zeros(len(data))

panet = []
pbnet = []
pcnet = []



filename = os.path.join(
    os.path.dirname(__file__),
    "ratio_data_new.csv"
)

while True:
    pa = 2661

    start = time()
    pa, pb, pc =  scope_obj.sample()
    end = time()
    #pa = np.array(pa).flatten()
    #pb = np.array(pb).flatten()


    panet.append(pa)
    pbnet.append(pb)
    pcnet.append(pc)

    if False:
        data+=np.histogram(pa, bins)[0]
        data2+=np.histogram(pb, bins)[0]

        plt.stairs(data, bins, label="Channel B")
        plt.stairs(data2, bins, label="Channel D")
        plt.xlabel("mV Signal", size=14)
        plt.ylabel("Counts", size=14)
        plt.show()

        
    #plt.plot(range(len(pa)), pa, label="max")
    #plt.plot(range(len(pb)), pb, label="min")
    #plt.show()
    print("Found  {}-B and {}-D {} seconds".format(pb/pa, pc/pa,  end-start))
    if (time() - begin)/90 > 1.:
        break

panet = np.array(panet)
pbnet = np.array(pbnet)
pcnet = np.array(pcnet)

if os.path.exists(filename):
    data = np.loadtxt(filename, delimiter=",")
    if len(np.shape(data))==1:
        data = [data,]
    else:
        data = data.tolist()
    data.append([time(), np.mean(pbnet/panet), np.std(pbnet/panet)/np.sqrt(len(pbnet)), np.mean(pcnet/panet), np.std(pcnet/panet)/np.sqrt(len(pcnet)) ])
else:
    data = [[time(),np.mean(pbnet/panet), np.std(pbnet/panet)/np.sqrt(len(pbnet)), np.mean(pcnet/panet), np.std(pcnet/panet)/np.sqrt(len(pcnet)) ],]

np.savetxt(filename, data, delimiter=",")

scope_obj.__exit__("arg")