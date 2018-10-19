#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 13:02:46 2018

@author: sm7gc
"""

import os
import time
import csv
import json 
import shutil
import gzip
from collections import defaultdict

## List of Device ID and Device Name pairs (ADD DEVICES AS NEEDED)
#device_dict = {"0d3a7c5044a5cc33": "Pixel2-walleye",
#               "fde44c748cd186a7":"Pixel2-taimen",
#               "A8375B1A-9B7E-4AFB-9E59-C0FFFBA294B8":"iPhone8.1",
#               "1a4cc41424b4d2a2":"LGE-elsa",
#               "5B668C42-B351-471B-BE64-9D485477A0EF":"iPhone9.1",
#               "6DD4FF11-386A-4092-B849-F8C3D1E4D6C5":"iPhone10.1"}


data_folder = 'D:/swear-test/10_19/raw' # Define data filepath(s)
target_folder = 'D:/swear-test/10_19/clean' # Define folder to store clean files

# Cuz I'm lazy
#shutil.rmtree(target_folder)
#os.makedirs(target_folder)

absolute_start_time = time.time()

complete_data = defaultdict(list)

filenames = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_folder) for f in filenames if os.path.splitext(f)[1] == '.gz']


for i in range(len(filenames)):
    
    file = filenames[i]

    #print("File " + str(i+1) + " out of " + str(len(filenames)) + ' (' + data_folder + ')') # progress print statement
    
    start_time = time.time()
    
    f = gzip.open(file, 'rb')
    file_content = f.read()
    raw_data = json.loads(file_content)

    base = ''
    if 'Swear' in file:
        base = 'Smartwatch_'

    for line in raw_data:
        
        line["Sensus OS"] = line["$type"].split(',')[1]
        line["Data Type"] = line.pop("$type").split(',')[0]
        
        if "PID" in line:
            line.pop("PID")
            
        data_type_split = line["Data Type"].split('.')
        data_type = data_type_split[len(data_type_split)-1]
        if data_type[-5:] == "Datum":
            datum = data_type[:-5]
        else:
            datum = data_type
            
        file = base + datum + '.csv'
        
        if datum == "Activity":
            line["Activity Mode"] = line.pop("Activity")

        complete_data[file].append(line)

    elapsed_time = time.time() - start_time
    elapsed_total_time = time.time() - absolute_start_time        
    
    print("--- " +  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) +  " / " + time.strftime("%H:%M:%S", time.gmtime(elapsed_total_time)) + " --- " %())


absolute_start_time = time.time()           
for key in complete_data.keys():
    
    print(key + ' (' + str(len(complete_data[key])) + ')') # progress print statement
    start_time = time.time()
    with open(os.path.join(target_folder,key),'w') as f:
        writer = csv.DictWriter(f, fieldnames=complete_data[key][0].keys(),lineterminator='\n')
        writer.writeheader()
        writer.writerows(complete_data[key])
        f.close()
        
    elapsed_time = time.time() - start_time
    elapsed_total_time = time.time() - absolute_start_time        
    
    print("--- " +  time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) +  " / " + time.strftime("%H:%M:%S", time.gmtime(elapsed_total_time)) + " --- " %())

print("Total Program Runtime: " + str(time.time() - absolute_start_time))