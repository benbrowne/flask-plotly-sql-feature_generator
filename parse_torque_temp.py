"""
- reads from stdin
- 'breaks the stream' when device or user defined time interval changes
- interval to generate features over is defined by the shell argument
- returns a dataframe to features.py
- features are defined by the user in features.py

data format:
 0	1420156760	drive_unit	{"torque": -0.025472679681420144, "temperature": 0.40841407648251765},
 0	1420156770	drive_unit	{"torque": 0.23807620959515494, "temperature": -1.1707010518041583},
 0	1420156780	drive_unit	{"torque": -0.08595670646206277, "temperature": 1.553783619625692},
 0	1420156790	drive_unit	{"torque": -0.9478755887865989, "temperature": 0.5052556076573897}]
"""

import sys
import json
import time
import numpy as np
import pandas as pd
import features

def parse_stdin(stdin):
    """generator of lines of data from stdin strings"""
    for line in stdin:
        device_id,epoch_time,data_type,json_data=line.strip('\n').split('\t')
        epoch_time=float(epoch_time)
        json_data=json.loads(data)
        torque=json_data['torque']
        temperature=json_data['temperature']
        yield (epoch_time,data_type,torque,temperature)


# we'll use these to check for new hours or devices
previous_hour=previous_device_id='none'

# the place we're going to accumulate data until device or hour changes:
columns=['epoch_time','data_type','torque','temperature']
#torque_temp_dataframe=pd.dataframe(columns=columns)

def get_features(stdin):
    # start reading the data
    for row_of_data in parse_stdin(stdin):
        hour = time.local_time(epoch_time).tm_hour
        # check if time or device have changed and if so return features and clear the dataframe
            if previous_hour != hour or previous_device_id!=device_id:
                df = pd.DataFrame(data_list,column=columns)
                yield {key:features.feature_input[key](df) for key in features.feature_input}
            else data_list.append(row_of_data)

    # note the time and device for comparison with the next iteration
        previous_device_id=device_id
        previous_hour=hour
