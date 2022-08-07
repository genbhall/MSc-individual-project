import pickle
from datetime import datetime, timedelta
from math import ceil
import numpy as np
import pandas as pd
from global_variables.global_variables import all_activities, start_date

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
        start_row = df[df['timestamp'] == anomalies['start'][anomaly]].index.values
        start_row = start_row[0]
        end_row = df[df['timestamp'] == anomalies['end'][anomaly]].index.values
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


# --------------------------------Anomaly Time<->date Conversion Formulae------------------------------------------ 

def convert_datetotime(date):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    time = int((date - start_date).total_seconds())
    return time

def convert_dfdatetotime(df):
    df['start'] = df['start'].apply(lambda x: convert_datetotime(x))
    df['end'] = df['end'].apply(lambda x: convert_datetotime(x))
    return df

def convert_timetodate(time):
    date = start_date + timedelta(seconds=time)
    return date

def convert_dftimetodate(df):
    df['start'] = df['start'].apply(lambda x: convert_timetodate(x))
    df['end'] = df['end'].apply(lambda x: convert_timetodate(x))
    return df


# --------------------------------Taken and adapted from Orion-ml---------------------------------------------------

def time_segments_aggregate(df, interval, time_column, method=['median']):

    #sorting the values on timestamp column and setting it as a index
    df = df.set_index(time_column)

    #corrects method argument if it is a string (puts it into a list of strings)
    if isinstance(method, str):
        method = [method]

    start_ts = df.index.values[0]
    max_ts = df.index.values[-1]

    values = list()
    index = list()
    while start_ts <= max_ts:
        end_ts = start_ts + interval
        subset = df.loc[start_ts:end_ts - 1]
        aggregated = [
            getattr(subset, agg)(skipna=True).values
            for agg in method
        ]
        values.append(np.concatenate(aggregated))
        index.append(start_ts)
        start_ts = end_ts

    return np.asarray(values), np.asarray(index)

def rolling_window_sequences(X, index, window_size, target_size, step_size, target_column,
                             drop=None, drop_windows=False):
    out_X = list()
    out_y = list()
    X_index = list()
    y_index = list()
    target = X[:, target_column]

    if drop_windows:
        if hasattr(drop, '__len__') and (not isinstance(drop, str)):
            if len(drop) != len(X):
                raise Exception('Arrays `drop` and `X` must be of the same length.')
        else:
            if isinstance(drop, float) and np.isnan(drop):
                drop = np.isnan(X)
            else:
                drop = X == drop

    start = 0
    max_start = len(X) - window_size - target_size + 1
    while start < max_start:
        end = start + window_size

        if drop_windows:
            drop_window = drop[start:end + target_size]
            to_drop = np.where(drop_window)[0]
            if to_drop.size:
                start += to_drop[-1] + 1
                continue

        out_X.append(X[start:end])
        out_y.append(target[end:end + target_size])
        X_index.append(index[start])
        y_index.append(index[end])
        start = start + step_size

    return np.asarray(out_X), np.asarray(out_y), np.asarray(X_index), np.asarray(y_index)
