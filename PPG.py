#readFileAndPlot.py]
import os
import sys
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from dateutil import tz
from dateutil import parser
import matplotlib.pyplot as plt
from scipy import signal
from datetime import timedelta
from sklearn.decomposition import FastICA, PCA

#######
def formatTimestamp(timestamp):
    
    timestamp = parser.parse(timestamp)
    
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    
    timestamp = timestamp.replace(tzinfo=from_zone)
    
    timestamp = timestamp.astimezone(to_zone)
    return timestamp

def windows(d, w, t):
    r = np.arange(len(d))
    s = r[::t]
    z = list(zip(s, s + w))
    f = '{0[0]}:{0[1]}'.format
    g = lambda t: d.iloc[t[0]:t[1]]
    #return pd.concat(map(g, z), keys=map(f, z))
    return map(g, z)

# Use numpy to load the data contained in the file
data = pd.read_csv('D:/swear-test/Smartwatch_PPG.csv')

omit_col = ['Sensus OS','Data Type','Device Model','DeviceId']
feat_df = data.drop(omit_col, axis=1)


data['Timestamp'] = data['Timestamp'].apply(lambda x: formatTimestamp(x))
data = data.set_index(['Timestamp'])
data = data.sort_index()

data['PPG1'].groupby(pd.Grouper(freq='S')).head()
dre = data['PPG1'].resample("10L").mean()
w= dre.rolling(600)
dre.shape
plt.plot(dre)
dre.head()
dre.to_csv('C:/Users/mob3f/Documents/Python Scripts/PPG.csv', sep=',')


dre3 = data.groupby(pd.TimeGrouper('10S'))['PPG1'].count()
dre2 = data.groupby(pd.TimeGrouper('5S'))['PPG1'].apply(lambda x: signal.resample(x, 500))
d = []
for key, value in dre2.items():
    i = 0
    time = key
    print('initial time ',key)
    for ppg in value:
        time = key + timedelta(milliseconds=i)
        i=i+10
        print(i,' ',time,' ', ppg)
        d.append({'Timestamp': time, 'PPG1': ppg})
clean=pd.DataFrame(d)
clean.shape
data.shape
clean = clean.set_index(['Timestamp'])
clean = clean.sort_index()
plt.plot(clean['PPG1'])
plt.plot(data['PPG1'])

wdf = windows(clean, 200, 20)
wdf.count()
ex= wdf.loc['0:200']
ex= wdf.loc['20:220']
ex= wdf.loc['40:240']
ex= wdf.loc['60:260']
plt.plot(ex)
w=0
for d in windows(clean, 200, 20):
    w=w+1
    if w==1:
        ica = FastICA(n_components=2)
        S_ = ica.fit_transform(d)  # Reconstruct signals
        A_ = ica.mixing_  # Get estimated mixing matrix 
        assert np.allclose(d, np.dot(S_, A_.T) + ica.mean_)
        p=d

plt.plot(d)
plt.plot(S_)
plt.plot(A_)
print(d)
    
dre3.std()
dre3.mean()
dre2[0].shape

f = signal.resample(data['PPG1'], 100)
f.shape
plt.plot(f[0], f[1], 'go-', f, '.-', 10, f[0], 'ro')
plt.show()


sampling_rate = 1 / np.diff(data['PPG1'])
sampling_rate = sampling_rate[~np.isnan(sampling_rate)]
sampling_rate.shape
np.histogram(sampling_rate,range=(0,500))
plt.hist(sampling_rate[0])
plt.plot(sampling_rate)


data = data.set_index(data[5].map(parser.parse))
# plot the first column as x, and second column as y
u = data[:,1]
t = data[:,5]
plt.figure(1)
plt.plot(t, u)
plt.title("Unfiltered PPG data")
plt.xlabel('Time[sec]')
plt.ylabel('PPG data')
plt.show()


#print size of u
print ("Size of data", u.size)

#### Bandpassfilter to filter out required frequencies for Heart Rate from PPG data
from scipy.signal import butter, lfilter


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y




 # Sample rate and desired cutoff frequencies (in Hz).
fs = 200
lowcut = 2
highcut = 6


# Filter the noisy signal.
y = butter_bandpass_filter(u, lowcut, highcut, fs, order=5)

plt.figure(2)
plt.plot(t, u, color ='crimson', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.ylabel('PPG data')
plt.title("Bandpass Filtered data for obtaining Heart Rate")
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()


#periodogram
N = u.size
FFT2 = abs(sc.fft(y,N))
f2 = 20*sc.log10(FFT2)
f2 = f2[range(N/2)] #remove mirrored part of FFT
freqs2 = sc.fftpack.fftfreq(N, t[1]-t[0])
freqs2 = freqs2[range(N/2)] #remove mirrored part of FFT


#Find highest peak in Periodogram
m = max(f2)
#Find corresponding frequency associated with highest peak
d =[i for i, j in enumerate(f2) if j == m]


#Plotting periodogram
x1 = freqs2[d]
y1 = max(f2)
plt.figure(3)
plt.subplot(2,1,1)
plt.plot(freqs2, f2,color='darkmagenta')
plt.ylabel("PSD")
plt.title('Periodogram for Heart Rate detection')
plt.grid()
plt.subplot(2,1,2)
plt.plot(freqs2,f2,color='turquoise')
plt.xlim((0,10))
plt.ylim((0,y1+20))
plt.text(x1,y1,'*Peak corresponding to Maximum PSD')
plt.xlabel('Frequency(Hz)')
plt.ylabel('PSD')
plt.grid()
plt.show()

##Print PSD and frequency
print ('Maximum PSD:' , max(f2))
print ("The frequency associated with maximum PSD is", freqs2[d], "Hz")

#Calculate Heart Rate
HeartRate = freqs2[d]*60
print ("Heart Rate  =", HeartRate, "Beats per minute")

##RESPIRATION RATE

# Filter requirements.
lowcut1 = 0.4
highcut1 = 0.7
fs3= 200
order3 = 3

# Filter the data, and plot both the original and filtered signals.
rr =butter_bandpass_filter(u, lowcut1, highcut1, fs, order3)
plt.figure(4)
plt.plot(t, u, color ='crimson', label='data')
plt.plot(t, rr, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.ylabel('PPG data')
plt.title('Bandpass Filtered Data for Respiration rate detection')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

##Periodogram 2
FFT3 = abs(sc.fft(rr,N))
f3 = 20*sc.log10(FFT3)
f3 = f3[range(N/2)]   #remove mirrored part of FFT
freqs3 = sc.fftpack.fftfreq(N, t[1]-t[0])
freqs3 = freqs3[range(N/2)]   #remove mirrored part of FFT



##calculate respiration rate

## Remove maximum PSD because it is at 0 Hz.
## Find best frequency
new = np.array(f3).tolist()
new.remove(max(new))
m3 = max(f3)
d3 =[i for i, j in enumerate(f3) if j == m3] ## the sample number associated to maximum PSD


##Plotting Periodogram 2
x2 = freqs3[d3]
y2 = m3
plt.figure(5)
plt.subplot(2,1,1)
plt.plot(freqs3, f3,linewidth = 2.5,color='firebrick')
plt.ylabel("PSD")
plt.title('Periodogram for Respiration Rate detection')
plt.grid()
plt.subplot(2,1,2)
plt.plot(freqs3, f3,linewidth = 2.5,color='darkolivegreen')
plt.xlim((0,2))
plt.ylim((0,y2+20))
plt.text(x2,y2,'*Peak corresponding to Best Frequency')
plt.grid()
plt.show()

## Print PSD and Frequency
print ('Maximum PSD for best frequency' , m3)
print ("Frequency corresponding to maximum PSD", freqs3[d3], "Hz")

#Calculate Respiration Rate
RespRate = freqs3[d3]*60

#print "Respiration Rate =", RespRate
print ("Respiration Rate  =", RespRate, "Breaths per minute")