from utils import Scope
from picosdk.ps3000a import ps3000a as ps

from time import time 
import matplotlib.pyplot as plt 
import numpy as np
import os 

#with Scope() as scope_obj:

scope_obj = Scope()
scope_obj.__enter__()
print(scope_obj)

scope_obj.enable_channel(0, collect = False)
scope_obj.set_trigger(0)

scope_obj.enable_channel(1)
scope_obj.enable_channel(3)

bins = np.linspace(0,400, 100)

data = np.zeros(len(bins)-1)
data2 = np.zeros(len(data))

panet = []
pbnet = []


begin = time()

filename = os.path.join(
    os.path.dirname(__file__),
    "data.csv"
)

while True:
    start = time()
    pa, pb =  scope_obj.sample()
    end = time()
    #pa = np.array(pa).flatten()
    #pb = np.array(pb).flatten()


    panet.append(pa)
    pbnet.append(pb)

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
    print("Found {} in A and {} in B in {}s".format(pa,pb, end-start))
    if (time() - begin)/50 > 0.5:
        break

if os.path.exists(filename):
    data = np.loadtxt(filename, delimiter=",")
    if len(np.shape(data))==1:
        data = [data,]
    else:
        data = data.tolist()
    data.append([time(), np.mean(panet), np.std(panet)/np.sqrt(len(panet)),np.mean(pbnet), np.std(pbnet)/np.sqrt(len(pbnet))])
else:
    data = [[time(), np.mean(panet), np.std(panet)/np.sqrt(len(panet)),np.mean(pbnet), np.std(pbnet)/np.sqrt(len(pbnet))],]

np.savetxt(filename, data, delimiter=",")

scope_obj.__exit__("arg")