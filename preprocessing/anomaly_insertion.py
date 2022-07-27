from global_variables.global_variables import filename, start_date

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

    #

    # pull anomaly from variable - maybe as a lost, activity, start, end
    # sleep anomaly - too long, too short, starting at the middle of the day, changing to smaller and smaller amounts
    # toilet anomalies - too long in the toilet, too many times a day 
    # not eating for a day
    # not drinking for a day
    # not taking morning meds

    start_date

def example_main():
    df = pd.read_csv(filename)
    df = change_series(sleep_in_anomaly, df)
    

if __name__ == "__main__":
    example_main()
