# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:28:18 2019

@author: mob3f
"""

import pandas as pd
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import get_time_domain_features,plot_poincare
import numpy as np


def windows(d, w, t):
    r = np.arange(len(d))
    s = r[::t]
    z = list(zip(s, s + w))
    f = '{0[0]}:{0[1]}'.format
    g = lambda t: d.iloc[t[0]:t[1]]
    #return pd.concat(map(g, z), keys=map(f, z))
    return map(g, z)

data = pd.read_csv('C:/Users/mob3f/Documents/ESME/results/Clean_Data/Smartwatch_HeartRate_clean.csv')

data['RR']= 60000/data.HR
time_domain_features = get_time_domain_features(data['RR'])

subjects=data.groupby(['DeviceId','condition'])
results = []
for name, group in subjects:
    print (name)
    for d in windows(group, 120, 60):
        time_domain_features = get_time_domain_features(d['RR'])
        time_domain_features['condition']=name[1]
        time_domain_features['participantId']=name[0]
        results.append(time_domain_features)

clean=pd.DataFrame(results)
clean.to_csv('C:/Users/mob3f/Documents/ESME/results/Clean_Data/Smartwatch_HRV.csv')
    
    
    conditions = group.groupby('condition')
    for condition,rest in conditions:
        
    
    group = group.set_index(pd.DatetimeIndex(group.index))
    resample_data = group.groupby(pd.TimeGrouper('5S'))
    for t,u in resample_data:
        if u.size>100:
            i = 0
            clean = signal.resample(u['PPG'], 500)
            for ppg in clean:
                time = t + timedelta(milliseconds=i)
                i=i+10
                closeind = np.argmin(np.abs(u.index - t))
                d.append({'PID':name,'Timestamp':time,'PPG':ppg,'Activity':u['Activity'][closeind]})
    
clean=pd.DataFrame(d)


plot_poincare(data['RR'])

