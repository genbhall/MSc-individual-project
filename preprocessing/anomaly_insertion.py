from global_variables.global_variables import filename_proc, all_activities, data_name, interval
import pandas as pd

#sleeps out of bed until 3am - only 4.20h sleep in bed - smaller anom
#brush teeth early then sleep out of bed (3.83h sleep) - big anom
#sleeps in until 10am - big anom
#sleeps out of bed until 1:50, then starts watching TV from 4:40 - big anom
#slept 9.4h - big anom
#slept 8.72h more than 1std
#slept 4.13h - should be lower rating
#slept 8.37h - should be lower rating 

existing_anomalies_hh101 = {
    'start': [
        '2012-08-22 00:00:00',
        '2012-08-24 03:47:00',
        '2012-08-29 07:00:00',
        '2012-08-30 00:00:00',
        '2012-09-01 07:00:00',
        '2012-09-04 00:00:00',
        '2012-09-14 00:00:00',
        '2012-09-15 00:00:00',
    ],
    'end': [
        '2012-08-22 08:00:00',
        '2012-08-24 07:00:00',
        '2012-08-29 10:00:00',
        '2012-08-30 05:00:00',
        '2012-09-01 10:00:00',
        '2012-09-04 09:00:00',
        '2012-09-14 08:00:00',
        '2012-09-15 08:00:00',
    ],
}

#Additional Synthetic Sleep Anomalies To include ------------------------------------------------------------

#Random 2.5h nap
sleep_random_anomaly = {
    'start': ['2012-09-08 14:00:00'],
    'end': ['2012-09-08 16:35:00'],
    'Activity': ['Sleep'],
}

#Wake up for an hour
sleep_break_anomaly = {
    'start': ['2012-09-12 02:30:00'],
    'end': ['2012-09-12 03:30:00'],
    'Activity': ['Watch_TV'],
}

#Additional Sleep Anomalies EXCLUDED ------------------------------------------------------------


#sleeps +5 hours longer - ALREADY EXISTS
sleep_in_anomaly_singlevar = {
    'start': [
        '2012-08-18 06:32:00',
        ],
    'end': [
        '2012-08-18 11:32:00',
        ],
    'Activity': [
        'Sleep',
        ],
}

#sleeps +3 hours longer
sleep_in_anomaly_multivar = {
    'start': [
        '2012-08-18 06:32:00',
        '2012-08-18 09:32:00',
        '2012-08-18 09:36:00',
        '2012-08-18 09:38:00',
        '2012-08-18 09:42:00',
        '2012-08-18 09:45:00',
        ],
    'end': [
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


#sleeps 3 hours later
sleep_late_anomaly = {
    'start': [
        '2012-09-11 00:57:00'
        ],
    'end': [
        '2012-09-11 03:57:00'
        ],
    'Activity': [
        'Watch_TV'
        ],
}

#no sleep
no_sleep_anomaly = {
    'start': [
        '2012-09-01 00:27:00'
        ],
    'end': [
        '2012-09-01 10:13:00'
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
    'end': [
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
    'end': [
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

# *Exclude section complete* -----------------------------------------------------------------


#synth_anomalies
synth_anomalies = [
    sleep_random_anomaly,
    sleep_break_anomaly
]

def anom_summary(anomaly):
    result = []
    length = len(anomaly['start'])
    result.append(anomaly['start'][0])
    result.append(anomaly['end'][length-1])
    return result

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
                while (df['Date'][row] != anomaly['end'][anom_tracker]):
                    for activity in all_activities:
                        if activity != 'timestamp':
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
    summary_anomalies = []
    for anomaly in synth_anomalies:
        insert_anomaly(anomaly, df)
        summary_anomaly = anom_summary(anomaly)
        summary_anomalies.append(summary_anomaly)
    df_sum = pd.DataFrame(summary_anomalies, columns= ['start', 'end'])
    df_known_sum = pd.DataFrame(existing_anomalies_hh101, columns= ['start', 'end'])
    df_sum = df_sum.append(df_known_sum)

    df.to_csv(f"processed_data/anomalous/{data_name}/{data_name}_anomalous_{interval}sw.csv")
    df_sum.to_csv(f"processed_data/anomalous/{data_name}/{data_name}_anomalous_{interval}sw_summary.csv")

if __name__ == "__main__":
    example_main()
