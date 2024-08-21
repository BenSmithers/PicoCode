import ctypes
from multiprocessing.sharedctypes import Value
from picosdk.ps3000a import ps3000a as ps
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc
from contextlib import ContextDecorator # used to trigger the compilation

from enum import Enum
import matplotlib.pyplot as plt 

import numpy as np 
import time as pytime
from scipy.signal import find_peaks

MAXSAMPLES = 25000
overflow = (ctypes.c_int16 * 60)()
cmaxSamples = ctypes.c_int32(MAXSAMPLES)
maxADC = ctypes.c_int16()

chARange = 5

channelInputRanges = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000]

class ReturnType(Enum):
    PulseCount = 0
    Amplitudes = 1
    Area = 2

class Scope(ContextDecorator):
    """
        We use the contextdecorator so that this will perform certain actions upon closing
    """

    def __enter__(self):
        self._channels={}
        self._threshs={}

        # Displays the staus returns
        self._prepared = False 
        self.chandle = ctypes.c_int16()
        self.status = ps.ps3000aOpenUnit(ctypes.byref(self.chandle ), None)
        self.powerstat =  ps.ps3000aChangePowerSource(self.chandle , 282)

        self._min_offset = 10 # ns? 
        self._max_offset = 20 
        self._time_per_sample = -1

    def __exit__(self, *exc):
        """
        We stop and close the connection to the picoscope 
        """
                
        # Stops the scope
        # Handle = chandle
        stat= ps.ps3000aStop(self.chandle)
        assert_pico_ok(stat)

        # Closes the unit
        # Handle = chandle
        stat = ps.ps3000aCloseUnit(self.chandle)
        assert_pico_ok(stat)

    def _prepare(self):
        """
            Prepare some memory stuff on the picoscope
            We don't want to do this until all of the channels are engaged though, so this function should be called before the bulk of sample happens 
        """
        timeIntervalns = ctypes.c_float()
        returnedMaxSamples = ctypes.c_int16()
        n_segments= 10*len(list(self._channels.keys()))
        print("Buffering {} segments".format(n_segments))
        status= ps.ps3000aGetTimebase2(self.chandle, 2, MAXSAMPLES, ctypes.byref(timeIntervalns), 1, ctypes.byref(returnedMaxSamples), 0)
        print("Using Time interval: {} ns".format(timeIntervalns))
        self._time_per_sample = float(timeIntervalns)

        assert_pico_ok(status)
        status=ps.ps3000aMemorySegments(self.chandle, n_segments, ctypes.byref(cmaxSamples))
        assert_pico_ok(status)
        status=ps.ps3000aSetNoOfCaptures(self.chandle, n_segments)
        assert_pico_ok(status)
        self._prepared = True 

    def enable_channel(self, channo, collect=True, pulse_threshold=40):
        """
            Enable the channel on the picoscope, and then prepare a Channel object where the buffers will be opened
        """
        print("enable channel, ", channo)
        status =ps.ps3000aSetChannel(self.chandle,channo, 1, 1, chARange, 0)
        assert_pico_ok(status)
        self._prepared = False
        if collect: 
            self._channels[channo] = Channel(self, channo)
            self._threshs[channo] = pulse_threshold
            return self._channels[channo]

    def disable_channel(self, channo):
        ps.ps3000aSetChannel(self.chandle,channo,0, 1, chARange, 0) 
        self._prepared = False 
        if channo in self._channels:
            del self._channels[channo]

    def set_trigger(self, channel, rising=True):
        print("Setting trigger", channel)
        status = ps.ps3000aSetSimpleTrigger(self.chandle, 1, channel, 1024, 2 if rising else 3, 0, 1000 )
        assert_pico_ok(status)


    def sample(self, return_kind=ReturnType.PulseCount):
        if not self._prepared:
            self._prepare()

        n_chan = len(list(self._channels.keys()))

        ps.ps3000aRunBlock(self.chandle, 0, MAXSAMPLES, 2, 1, None, 0, None, None)

        peaks = [0 for _ in self._channels.keys()]
        amps = [[] for _ in self._channels.keys()]
        times = [[] for _ in self._channels.keys()]

        for ic, chankey in enumerate(self._channels.keys()):
            for bx in range(len(self._channels[chankey].bufmin)):
                
                buffer_no = bx #+ic*len(self._channels[chankey].bufmin)
                status = ps.ps3000aSetDataBuffers(self.chandle, chankey, self._channels[chankey].bufmax[bx].ctypes.data, self._channels[chankey].bufmin[bx].ctypes.data, MAXSAMPLES, buffer_no, ps.PS3000A_RATIO_MODE["PS3000A_RATIO_MODE_NONE"] )
                assert_pico_ok(status)

        ready = ctypes.c_int(0)
        check = ctypes.c_int(0)
        bad_count =0
        while ready.value==check.value:
            status = ps.ps3000aIsReady(self.chandle, ctypes.byref(ready))
            pytime.sleep(0.02)
            if bad_count>40:
                assert_pico_ok(status)  
                if status==0:
                    break
                raise ValueError()
            bad_count+=1

        status = ctypes.c_int(1)
        while status!=0:
            # ps.ps3000aGetValuesBulk(chandle, ctypes.byref(cmaxSamples), 0, 9, 1, 0, ctypes.byref(overflow))
            status = ps.ps3000aGetValuesBulk(self.chandle, ctypes.byref(cmaxSamples), 0, 9,  0, ps.PS3000A_RATIO_MODE["PS3000A_RATIO_MODE_NONE"] , ctypes.byref(overflow))
            pytime.sleep(0.05)
        assert_pico_ok(status)  
        status = ps.ps3000aMaximumValue(self.chandle, ctypes.byref(maxADC))
        assert_pico_ok(status)



        for ic, chankey in enumerate(self._channels.keys()):  
            sign = 1 if chankey==0 else -1
            for i in range(10):
                parsed = adc2mV(self._channels[chankey].bufmax[i], chARange, maxADC)
                #plt.plot(range(len(parsed)), sign*np.array(parsed), alpha=0.2)
                
                # find_peks returns only the index of the peaks, so we need to extrapolate out to get a time
                # and then also consider that each of these samples are sequential
                peakfind = find_peaks(sign*np.array(parsed), height=self._threshs[chankey])
                shifted_times = np.array(peakfind[0])*self._time_per_sample + i*self._time_per_sample*len(parsed)

                peaks[ic] += len(peakfind[0])
                times[ic] += shifted_times.tolist() 
                amps[ic] += list(peakfind[1]["peak_heights"])
                
        accepted = [[], []]
        # iterate over the pulse times for channels
        for pulse_time in range(len(times[1])):
            # binary search to find the trigger pulses bordering this one
            index = np.searchsorted(times[0], pulse_time)-1  # minus one to get the proper index of the proceeding pulse 
            tdiff = pulse_time - times[0][index]
            accepted[0].append( tdiff>self._min_offset and tdiff<self._max_offset )
        
        for pulse_time in range(len(times[[2]])):
            index = np.searchsorted(times[0], pulse_time)-1  # minus one to get the proper index of the proceeding pulse 
            tdiff = pulse_time - times[0][index]
            accepted[1].append( tdiff>self._min_offset and tdiff<self._max_offset )
        
        accepted = np.array(accepted)

        #return self._channels[chankey].bufmax[i], self._channels[chankey].bufmin[i]
        #plt.show()
        if return_kind==ReturnType.PulseCount:
            return len(amps[0][accepted]),len(amps[1][accepted])  
        elif return_kind==ReturnType.Amplitudes:
            return amps[0][accepted], amps[1][accepted]

    def adc2mV(self, bufferADC, maxADC):
        bufferV = bufferADC*channelInputRanges[chARange]/maxADC
        return bufferV

class Channel:
    """
        the scope of this class evolved as the code was written. 
        Right now, it's just an object for holding the buffers for the channels
        It may evolve down the line though
    """
    def __init__(self, scope:Scope, channel:int):
        """
            channel - 0, 1, 2, 3 
            for A, B, C, and D 
        """
 
        self.bufmin = [np.empty(MAXSAMPLES,dtype=np.dtype('int16')) for i in range(10)]
        self.bufmax = [np.empty(MAXSAMPLES,dtype=np.dtype('int16')) for i in range(10)]
        
