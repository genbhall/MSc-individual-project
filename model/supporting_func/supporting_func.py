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

#Function returns df into numpy split of values and index at interval time slots 
def time_segments_aggregate(df, interval, time_column, method=['mean']):

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
        
        #this gets the mean value per category and sets that as the value for set time
        aggregated = [
            getattr(subset, agg)(skipna=True).values
            for agg in method
        ]
        values.append(np.concatenate(aggregated))
        index.append(start_ts)
        start_ts = end_ts

    return np.asarray(values), np.asarray(index)

#converts aggregate values/index into array of windows of window size
def rolling_window_sequences(x_values, index, window_size, target_size, step_size, 
                             target_column):
    
    out_X = list()
    out_y = list()
    X_index = list()
    y_index = list()
    target = x_values[:, target_column]

    start = 0
    
    #create the respective lists for output
    max_start = len(x_values) - window_size - target_size + 1
    while start < max_start:
        end = start + window_size
        out_X.append(x_values[start:end])
        out_y.append(target[end:end + target_size])
        X_index.append(index[start])
        y_index.append(index[end])
        start = start + step_size

    return np.asarray(out_X), np.asarray(out_y), np.asarray(X_index), np.asarray(y_index)

#collapses each window input sequence into output array (using median at each time point)
def collapse_ts(x_values_hat):
    predictions = list()
    
    #length of each input sequence
    pred_length = x_values_hat.shape[1]
    
    #length of entire dataset
    num_errors = x_values_hat.shape[1] + (x_values_hat.shape[0] - 1)

    #for each value in the length of dataset - take the median
    for i in range(num_errors):
            intermediate = []

            #for every relevant prediction in input, append it to the intermediate
            for j in range(max(0, i - num_errors + pred_length), min(i + 1, pred_length)):
                intermediate.append(x_values_hat[i - j, j])

            #and if there is anything in the intermediate, then take the median and add to predictions
            if intermediate:
                predictions.append(np.median(np.asarray(intermediate)))

    #return the predictions for each time point
    return np.asarray(predictions[pred_length-1:])

#calculates thresholds above a certain frequency
def anomalies_calc(threshold, error_array, index):
    intervals = list()
    i = 0
    max_start = len(error_array)
    
    #for each timeslot, if error is above threshold, add it to the intervals list
    while i < max_start:
        j = i
        start = index[i]
        while (i < max_start) and (error_array[i] > threshold):
            i += 1
        
        end = index[i]
        if start != end:
            intervals.append((start, end, np.mean(error_array[j: i+1])))          
        i += 1
    
    return intervals