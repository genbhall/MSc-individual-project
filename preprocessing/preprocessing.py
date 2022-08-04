import pandas as pd
import numpy as np
import datetime

pd.options.mode.chained_assignment = None  # default='warn'

#takes in dataframe from HH series - adds new column in pandas with cumulative time across the dataset
def create_cumulativeTime_col(df):
    
    #create a cumulative time column
    df['cumulativeTime'] = df['timeSinceLastSensorEvent'].cumsum()
    df['cumulativeTime'] += df['lastSensorEventSeconds'][0]
    
    #return the new df
    return df

#helper function - adds key to dict with value 0 if not yet in dict
def add_to_dict(dictionary,key):
    if key not in dictionary:
        dictionary[key] = 0

#takes pandas df, returns dictionary of time: activity in x second intervals
def convert_to_timeseries(df, interval, col_time, col_activity):

    # get the beginning and end value for the last element in the timeseries 
    # nb - activity gets added to the 60 seconds previous to the timestamp
    max_time = (int(df[col_time].max() / interval) +1) * interval 
    min_time = (int(df[col_time].min() / interval) + 1) * interval

    # create new timeseries dataframe with activities as input
    activity_array = df[col_activity].unique()
    activity_array = np.insert(activity_array,0,'timestamp')
    activity_array = np.insert(activity_array,1,'hour_day')
    ts_df = pd.DataFrame(columns=activity_array)

    row_tracker = 0
    df_tracker = 0
    SECONDS_IN_DAY = 3600 * 24
    SECONDS_IN_HOUR = 60

    for time_t in range(min_time, max_time, interval):

        # create new rows in dataframe - all 0s, set time to timestamp
        ts_df = ts_df.append(pd.Series(0, index=ts_df.columns), ignore_index=True)
        ts_df['timestamp'][df_tracker] = time_t
        ts_df['hour_day'][df_tracker] = int((time_t % SECONDS_IN_DAY) / SECONDS_IN_HOUR)
        print(ts_df['hour_day'][df_tracker])

        #next lines is to find the dominant activity in the time slot and add it to the tracker
        activities_dict = {}
        
        # this is to gather the remaining seconds activity from previous search
        if row_tracker > 0:
            
            # add the last activity of previous search to the dictionary if it does not already exist
            add_to_dict(activities_dict,df[col_activity][row_tracker-1])

            # add that remaining time to the dictionary
            activities_dict[df[col_activity][row_tracker]] = df[col_time][row_tracker] - (time_t - interval)

        # Then move to next activities
        # This gets the range of rows that fall into the range of the time bracket. (exclusive end)
        while df[col_time][row_tracker] < time_t:
                
            # add the activity to the dictionary if it does not already exist
            add_to_dict(activities_dict,df[col_activity][row_tracker])

            # get the incremental time the activity has been going on from since previous row
            activity_seconds = 0    
            if df[col_time][row_tracker+1] < time_t:
                activity_seconds = df[col_time][row_tracker+1] - df[col_time][row_tracker]
            else:
                activity_seconds = time_t - df[col_time][row_tracker]

            # then add it onto the dictionary of activities for the category
            activities_dict[df[col_activity][row_tracker]] += activity_seconds

            # increment the row
            row_tracker += 1

        # now select the highest weighted activity in the dictionary
        activity = max(activities_dict, key=activities_dict.get)
        
        #set time stamp and target activity to 1 
        ts_df[activity][df_tracker] = 1

        df_tracker += 1

    return ts_df

def add_datetime_column(df, start_date):

    df['Date'] = df['timestamp'].apply(lambda date: start_date + datetime.timedelta(seconds = date))
    col_to_move = df.pop('Date')
    df.insert(1,"Date",col_to_move)
    return df
