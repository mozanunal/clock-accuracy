
# coding: utf-8

# In[1]:


import numpy as np
from scipy.signal import find_peaks, find_peaks_cwt
import soundfile as sf
from matplotlib import pyplot as plt

get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


def printShift(shift):
    """
    param shift: should be in second
    """
    shiftInDay = 24*3600*shift
    print("Shift: {} us".format(shift*1000000))
    print("Shift in day: {} s".format(shiftInDay))


# In[3]:


def calculateAccuracy(filename):
    data, samplerate = sf.read(filename)
    if len(np.shape(data)) > 1: # Streo check
        ch1 = data[:,0]
    else:
        ch1 = data
    print("Filename: {}".format(filename))
    print("Samplerate: {}".format(samplerate))
    print("Min Resolution: {} us".format(1000000*(1/samplerate)))
    print("Lenght: {} - {} s".format(len(ch1), len(ch1)/samplerate))
    peaks, t= find_peaks(ch1, height=0.01, distance=samplerate-500)
    peaksTime = peaks* (1/samplerate)
    
    """
    Method 1
    """
    #peaksNo = len(peaks)-1
    #shift = ((peaksTime[peaksNo] - peaksTime[0]) - peaksNo) / peaksNo
    #printShift(shift)
    """
    Method 2
    """
    shiftList = []
    sumS = 0
    for i in range(0,len(peaksTime)-1):
        s = peaksTime[i] - peaksTime[i+1] +1
        print(s)
        if np.abs(s) < 0.005:
            sumS += s
            shiftList.append( s )
    shift = sumS / len(shiftList)
    printShift(shift)
    
    #fftPlot(ch1,samplerate)
    plt.figure()
    plt.plot(ch1)
    plt.plot(peaks, ch1[peaks], "x")
    
    
    


# In[4]:


def fftPlot(ch1, samplerate):
    freq = np.arange(0,samplerate, samplerate/len(ch1))
    plt.figure()
    plt.plot(freq, np.fft.fft(ch1))
    #plt.xlim(0,100)


# In[5]:


calculateAccuracy("test1.wav")


# In[6]:


calculateAccuracy("test2.wav")

