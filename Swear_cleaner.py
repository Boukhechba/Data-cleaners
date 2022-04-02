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
import numpy as np
import traceback



data_folder = 'C:/Users/mob3f/Google Drive/Projects/Fluisense/2021-01-23/Unknown/' # Define data filepath
target_folder = 'C:/Users/mob3f/Google Drive/Projects/Fluisense/2021-01-23/Unknown' # Define folder to store clean files


absolute_start_time = time.time()

complete_data = defaultdict(list)

filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_folder) for f in filenames if f.endswith('.gz')]


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
    i=1
    print(os.path.getsize(file))
    if os.path.getsize(file) > 0:
        for l in lines:
            if i < len(lines)-1:
                obj=l[:-2]
            i=i+1
            try:
                line=json.loads(obj)

                data_type = line.pop("TP")
                datum = data_type
                line["ParticipantId"] = file.split('_')[2]
                line["FileCreationTime"] = file.split('_')[4]
                line["DeviceId"] = file.split('_')[3]

                if "PID" in line:
                    line.pop("PID")
                    
                    
                filename_out = base + datum + '.csv'
                
                if datum == "Activity":
                    line["Activity Mode"] = line.pop("Activity")
                complete_data[filename_out].append(line)
                
            except Exception as e:
                print(e)
#                traceback.print_exc()
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
