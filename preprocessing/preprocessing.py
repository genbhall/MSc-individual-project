import pandas as pd
import numpy as np
from datetime import date

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
    activity_array = np.insert(activity_array,0 ,'Time')
    ts_df = pd.DataFrame(columns=activity_array)

    print(df)
    row_tracker = 0

    # first test with value, then loop across all.
    time_t = min_time
    # for time in range(min_time, max_time, interval):

    activities_dict = {}
    
    print(time_t)

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

        print(activity_seconds)
        # then add it onto the dictionary of activities for the category
        activities_dict[df[col_activity][row_tracker]] += activity_seconds

        # increment the row
        row_tracker += 1

    #now select the highest weighted activity in the dictionary
    activity = max(activities_dict, key=activities_dict.get)
    print(activity)    

        #get all the rows within the range
