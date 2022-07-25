import pickle
from datetime import datetime, timedelta
from math import ceil
import numpy as np

#Saves model weights and biases
def save_model(trained_model):
    with open('trained_model.pickle', 'wb') as target:
        pickle.dump(trained_model, target)
    print("\nSaved model in trained_model.pickle\n")

#loads the appropriate pickle file
def load_model():
    with open('trained_model.pickle', 'rb') as target:
        trained_model = pickle.load(target)
    print("\nLoaded model in trained_model.pickle\n")
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
