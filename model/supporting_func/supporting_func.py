import pickle
from datetime import datetime, timedelta
from math import ceil
import numpy as np
from global_variables.global_variables import all_activities
import pandas as pd

#Saves model weights and biases - name excludes folder
def save_model(trained_model, name):
    picklefile = f"saved_models/{name}"
    with open(picklefile, 'wb') as target:
        pickle.dump(trained_model, target)
    print(f"\nSaved model in {picklefile}\n")

#loads the appropriate pickle file - name excludes folder
def load_model(name):
    picklefile = f"saved_models/{name}"
    with open(picklefile, 'rb') as target:
        trained_model = pickle.load(target)
    print(f"\nLoaded model in {picklefile}\n")
    return trained_model

#split data into groups of times based on days interval. 
#Returns dictionary of intervals - date input is name of Date column
def split_data(df, interval, date='Date'):
    start_date = datetime.strptime(df[date].min(), '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(df[date].max(), '%Y-%m-%d %H:%M:%S')
    delta = (end_date - start_date).days + 1
    splits = ceil(delta/interval)

    dict_pd = {}
    end_interval = start_date.date() + timedelta(days=interval)
    total_rows = df.shape[0]
    start_row = 0
    count = start_row
    count_date = datetime.strptime(df[date][count], '%Y-%m-%d %H:%M:%S').date()

    #for each interval 
    for num in range(0,splits):
                
        #find last row lower than interval
        while ((count_date < end_interval) and (count < (total_rows-1))):
            count += 1
            count_date = datetime.strptime(df[date][count], '%Y-%m-%d %H:%M:%S').date()

        dict_pd[num] = df.iloc[start_row:count, :]
        start_row = count

        #move onto the next iteration of start / end intervals
        start_date = end_interval
        end_interval = start_date + timedelta(days=interval)
        
    return dict_pd

#takes anomalies dataFrame and breaks out all interactions within labeled anomaly
def print_anomalies(anomalies, filename):
    df = pd.read_csv(filename)

    anomaly_dict = {}

    #for each anomaly
    for anomaly in range(0,anomalies.shape[0]):
        start_row = df[df['Time'] == anomalies['start'][anomaly]].index.values
        start_row = start_row[0]
        end_row = df[df['Time'] == anomalies['end'][anomaly]].index.values
        end_row = end_row[0]
        anomaly_details = {
            'Activity': [],
            'Start': [],
            'Stop': [],
        }
        current_activity = ''
        first_tracker = 1
        time_tracker = 0

        for row in range(start_row,end_row):

            #get the activity and the time
            for activity in all_activities:
                if ((df[activity][row] == 1) and (activity != current_activity)):
                    anomaly_details['Activity'].append(activity)
                    anomaly_details['Start'].append(df['Date'][row])
                    anomaly_details['Stop'].append(df['Date'][row-1])
                    current_activity = activity
                    if first_tracker:
                        anomaly_details['Stop'].pop()
                        first_tracker -= 1

            #append end time to last activity    
            if row == end_row-1:
                anomaly_details['Stop'].append(df['Date'][row])
        
        #convert anomaly_detials to pandas and append
        anomaly_dict[anomaly] = pd.DataFrame(anomaly_details)
        print(anomaly_dict[anomaly])

    return anomaly_dict