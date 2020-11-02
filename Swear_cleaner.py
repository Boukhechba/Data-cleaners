# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 12:16:09 2020

@author: mehdi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 13:02:46 2018

@author: Mehdi
"""

import os
import time
import csv
import json 
import pandas as pd
import gzip
from collections import defaultdict
import jsonlines
import numpy as np



data_folder = 'C:/Users/mehdi/Documents/My_projects/mhealth_class/sleep/raw' # Define data filepath
target_folder = 'C:/Users/mehdi/Documents/My_projects/mhealth_class/sleep/clean' # Define folder to store clean files


absolute_start_time = time.time()

complete_data = defaultdict(list)

filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_folder) for f in filenames if f.endswith('.json')]


for i in range(len(filenames)):
    
    file = filenames[i]

    print("File " + str(i+1) + " out of " + str(len(filenames)) + ' (' + data_folder + ')'+ ' (' + file + ')') # progress print statement
#    try:
    start_time = time.time()
    if (file.endswith(".gz")):
        f = gzip.open(file, 'rb')
    elif(file.endswith(".json")):
        f = open(file)
#    file_content = f.read()
#    raw_data = json.loads(file_content)
    base = ''
    if 'Swear' in file:
        base = 'Smartwatch_'
    else:
        base = 'Sensus_'
        
    data=[]
    lines = f.readlines()
    print (len(lines))
    i=1
    for l in lines:
        if i < len(lines)-1:
            obj=l[:-2]
        i=i+1
        try:
            line=json.loads(obj)
            if ( 'Swear' in file):
                data_type = line.pop("TP")
                datum = data_type
                line["ParticipantId"] = file.split('_')[3]
                line["FileCreationTime"] = file.split('_')[5]
                line["DeviceId"] = file.split('_')[4]
            else:
                line["Sensus OS"] = line["$type"].split(',')[1]
                line["Data Type"] = line.pop("$type").split(',')[0]
                data_type_split = line["Data Type"].split('.')
                data_type = data_type_split[len(data_type_split)-1]
                if data_type[-5:] == "Datum":
                    datum = data_type[:-5]
                else:
                    datum = data_type
            if "PID" in line:
                line.pop("PID")
                
                
            filename_out = base + datum + '.csv'
            
            if datum == "Activity":
                line["Activity Mode"] = line.pop("Activity")
            complete_data[filename_out].append(line)
        except:
            print(obj)
         
    for key in complete_data.keys():
        print (key)
        if not (os.path.isfile(os.path.join(target_folder,key))):
            w = open(os.path.join(target_folder,key),'a',encoding='utf-8')
            writer = csv.DictWriter(w, fieldnames=complete_data[key][0].keys(),lineterminator='\n')
            writer.writeheader()
        w = open(os.path.join(target_folder,key),'a', encoding='utf-8')
        writer = csv.DictWriter(w, fieldnames=complete_data[key][0].keys(),lineterminator='\n')
        writer.writerows(complete_data[key])
    complete_data.clear()
    w.flush()
    elapsed_time = time.time() - start_time
    elapsed_total_time = time.time() - absolute_start_time        
        
    print("--- " +  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) +  " / " + time.strftime("%H:%M:%S", time.gmtime(elapsed_total_time)) + " --- " %())
#    except:
#        print("File corrupted")
    
f.close()
w.close()
