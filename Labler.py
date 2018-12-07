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
data = pd.read_csv('D:/WASH/Swear/clean/Smartwatch_PPGDatum.csv')