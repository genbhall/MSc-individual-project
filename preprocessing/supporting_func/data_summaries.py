
from re import I
import pandas as pd
from datetime import datetime, timedelta

#takes an activity, return pandas version of 
def strip_activity(activity, df_input):
    
    #create the output df
    sleeping = False
    i=0
    max_index = len(df_input)-1
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
        
        #iterate through each row
        for i in range(length):
            row_time = df_sleep['start'][i]
            if (row_time < end) and (row_time > start):
                total_sleep = total_sleep + df_sleep['Duration'][i]
                sleep_count += 1
        
        intermediate.append(total_sleep)
        intermediate.append(sleep_count)
        intervals.append(intermediate)

        start = start + timedelta(days=1)
        end = end + timedelta(days=1)

    columns = ['Date-nightof','total_sleep', 'sleep_count']
    df_output = pd.DataFrame(intervals, columns=columns)

    return df_output