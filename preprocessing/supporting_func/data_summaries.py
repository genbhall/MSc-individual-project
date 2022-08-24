import pandas as pd
from datetime import datetime, timedelta
from math import ceil
import numpy as np

#takes an activity, return pandas version of 
def strip_activity(activity, df_input):
    
    #create the output df
    sleeping = False
    i=df_input.index.tolist()[0]
    max_index = df_input.index.tolist()[-1]
    intervals = list()

    while i < max_index:
        #skips row to sleep stage
        while (i < max_index) and (df_input[activity][i] != 1):
            i += 1

        if (df_input[activity][i] == 1):

            #if got here, first time sleep
            intermediate = []
            start_date = datetime.strptime(df_input['Date'][i], '%Y-%m-%d %H:%M:%S')
            intermediate.append(activity)
            intermediate.append(start_date)

            #then go to the end of the sleep session
            while (i < max_index) and (df_input[activity][i] == 1):
                i += 1
            
            #will overshoot so reduce to last point
            i-=1
            end_date = datetime.strptime(df_input['Date'][i], '%Y-%m-%d %H:%M:%S')
            intermediate.append(end_date)
            duration = end_date - start_date
            duration = duration.days*24 + duration.seconds/3600
            intermediate.append(duration)
            intervals.append(intermediate)

            #move to next row
            i += 1

    columns = ['Activity','start', 'end', 'Duration']
    df_output = pd.DataFrame(intervals, columns=columns)

    return df_output

#combines all sleep from a particular data into one entry in a pandas dataframe
def combine_sleep(df_sleep, start_date, end_date):
    
    intervals = list()
    total_days = (end_date - start_date).days
    start = start_date.replace(hour=12,minute=0)
    length = len(df_sleep)-1

    for day in range(total_days):
        intermediate = []
        total_sleep = 0
        sleep_count = 0
        intermediate.append(start)
        end = start + timedelta(days=1)
        first_sleep_bool = True
        first_sleep = str()
        last_sleep = str()
        
        #iterate through each row
        for i in range(length):
            row_time = df_sleep['start'][i]
            if (row_time < end) and (row_time > start):
                if first_sleep_bool:
                    first_sleep = df_sleep['start'][i].strftime("%H:%M:%S")
                    first_sleep_bool = False
                total_sleep = total_sleep + df_sleep['Duration'][i]
                last_sleep = df_sleep['end'][i].strftime("%H:%M:%S")
                sleep_count += 1
        intermediate.append(round(total_sleep,2))
        intermediate.append(first_sleep)
        intermediate.append(last_sleep)
        intermediate.append(sleep_count)
        intervals.append(intermediate)

        start = start + timedelta(days=1)
        end = end + timedelta(days=1)

    columns = ['Date','total_sleep','first_sleep','last_sleep', 'sleep_count']
    df_output = pd.DataFrame(intervals, columns=columns)

    return df_output

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

#converts array of time strings to time of day (EXCLUDES EMPTY CELLS)
def convert_to_hours(array, night_time=True):
    result = []
    for i in array:
        if i != '':
            i_date = datetime.strptime(i, '%H:%M:%S')
            hours = i_date.hour + i_date.minute/60 + i_date.second/(60*60)

            #this is if sleeping after 12 that day - make it go up
            if (hours < 12 and night_time):
                hours = hours + 24
            result.append(hours)
        else:
            result.append(np.nan)
    result = np.asarray(result)
    return result
