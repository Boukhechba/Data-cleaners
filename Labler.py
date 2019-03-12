# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 17:18:09 2018

@author: mob3f
"""
import pandas as pd
from datetime import datetime
from dateutil import tz
from dateutil import parser

def formatTimestamp(timestamp):
    
    timestamp = parser.parse(timestamp)
    
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    
    timestamp = timestamp.replace(tzinfo=from_zone)
    
    timestamp = timestamp.astimezone(to_zone)
    return timestamp


gt = pd.read_csv('D:/WASH/Swear/DataCollection.csv')
gt['T_s'] = pd.to_datetime(gt['T_s'])
gt['T_f'] = pd.to_datetime(gt['T_f'])
data = pd.read_csv('D:/WASH/Swear/clean/Smartwatch_PPGDatum.csv')
data['Timestamp']=pd.to_datetime(data['Timestamp'])
size=data.shape()
#data['Timestamp'] = data['Timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')
data.describe
for index, row in data.iterrows():
    for g,truth in gt.iterrows():
        if row['Timestamp']>=truth['T_s'] and row['Timestamp']<=truth['T_f']:
            data.at[index, 'Activity'] = truth['Activity']
            data.at[index, 'PID'] = truth['PID']
   