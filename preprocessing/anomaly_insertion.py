from global_variables.global_variables import filename_proc, all_activities, data_name, interval
import pandas as pd

#sleeps +3 hours longer
sleep_in_anomaly = {
    'start': [
        '2012-08-18 06:32:00',
        '2012-08-18 09:32:00',
        '2012-08-18 09:36:00',
        '2012-08-18 09:38:00',
        '2012-08-18 09:42:00',
        '2012-08-18 09:45:00',
        ],
    'stop': [
        '2012-08-18 09:32:00',
        '2012-08-18 09:34:00',
        '2012-08-18 09:38:00',
        '2012-08-18 09:42:00',
        '2012-08-18 09:45:00',
        '2012-08-18 10:00:00',
        ],
    'Activity': [
        'Sleep',
        'Toilet',
        'Other_Activity',
        'Personal_Hygeine',
        'Cook_Breakfast',
        'Eat_Breakfast',
        ],
}

#does not sleep day
sleep_random_anomaly = {
    'start': ['2012-08-26 12:17:00'],
    'stop': ['2012-08-26 16:41:00'],
    'Activity': ['Sleep'],
}

#sleeps 3 hours later
sleep_late_anomaly = {
    'start': [
        '2012-09-11 00:57:00'
        ],
    'stop': [
        '2012-09-11 03:57:00'
        ],
    'Activity': [
        'Watch_TV'
        ],
}

#uses toilet per day +4 times in the morning - CONTEXTUAL
toilet_anomaly = {
    'start': [
        '2012-09-05 08:09:00', 
        '2012-09-05 09:06:00',
        '2012-09-05 09:51:00',
        '2012-09-05 10:33:00',
        ],
    'stop': [
        '2012-09-05 08:12:00', 
        '2012-09-05 09:08:00',
        '2012-09-05 09:54:00',
        '2012-09-05 10:37:00', 
        ],
    'Activity': [
        'Toilet', 
        'Toilet', 
        'Toilet', 
        'Toilet'
        ],
}

#does not eat for a day
eating_anomaly = {
    'start': [
        '2012-08-31 07:49:00', 
        '2012-08-31 14:48:00', 
        '2012-08-31 19:56:00'
        ],
    'stop': [
        '2012-08-31 08:17:00',
        '2012-08-31 15:01:00', 
        '2012-08-31 20:24:00'
        ],
    'Activity': [
        'Read', 
        'Other_Activity', 
        'Watch_TV'
        ],
}

# takes in pandas list of anomalies - changes pandas dataframe to reflect new anomaly
# anomalies structured as "activity, start, end"
def insert_anomaly(anomaly,df):

    #convert to pandas
    anomaly = pd.DataFrame(anomaly)
    anom_length = anomaly.shape[0]
    df_length = df.shape[0]
    anom_tracker = 0
    row = 0

    #for each row in the df
    while row < df_length:

        #if matches one of the changed anomalies - change the data
        if anom_tracker < anom_length:
            if (df['Date'][row] == anomaly['start'][anom_tracker]):
                while (df['Date'][row] != anomaly['stop'][anom_tracker]):
                    for activity in all_activities:
                        if activity != 'Time':
                            if activity != anomaly['Activity'][anom_tracker]:
                                df.loc[row, activity] = 0
                            else:
                                df.loc[row, activity] = 1
                    row += 1

                #iterate to new activity change
                anom_tracker += 1
                row -= 1
        row += 1

def example_main():
    df = pd.read_csv(filename_proc)
    print(df.shape[0])

    insert_anomaly(sleep_in_anomaly, df)
    insert_anomaly(sleep_random_anomaly, df)
    insert_anomaly(sleep_late_anomaly, df)
    insert_anomaly(toilet_anomaly, df)
    insert_anomaly(eating_anomaly, df)

    df.to_csv(f"processed_data/anomalous/{data_name}/{data_name}_anomalous_{interval}sw.csv")

if __name__ == "__main__":
    example_main()
