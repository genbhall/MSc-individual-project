from turtle import st
from global_variables.global_variables import filename_proc, all_activities, data_name, interval
import pandas as pd

#sleeps too much - first test on one variable, then test on all
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

#sleeps at weird time
sleep_random_anomaly = {
    'start': ['2012-08-18 06:32:00'],
    'stop': ['2012-08-18 09:32:00'],
    'Activity': ['Sleep'],
}

#does not sleep day
no_sleep_anomaly = {
    'start': ['2012-08-18 06:32:00'],
    'stop': [],
    'Activity': ['Sleep'],
}

#uses toilet < per day
toilet_anomaly = {
    'start': [],
    'stop': [],
    'Activity': ['Toilet'],
}

#does not eat for a day
eating_anomaly = {
    'start': [],
    'stop': [],
    'Activity': ['Dinner'],
}


# takes in pandas list of anomalies - changes pandas dataframe to reflect new anomaly
# anomalies structured as "activity, start, end"
def change_series(anomaly,df):

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
    change_series(sleep_in_anomaly, df)
    print(df.loc[41511:41718, :])
    df.to_csv(f"processed_data/anomalous/{data_name}/{data_name}_anomalous_{interval}sw.csv")

if __name__ == "__main__":
    example_main()
