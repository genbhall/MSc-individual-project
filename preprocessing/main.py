import pandas as pd
from preprocessing import create_cumulativeTime_col, convert_to_timeseries

def example_main():

    #target variables (to change if necessary)
    filename = "../CASAS_dataset/23_HH101/hh101.ann.features.csv"
    column_headers = ['lastSensorEventHours', 'lastSensorEventSeconds', 'lastSensorDayOfWeek',
       'windowDuration', 'timeSinceLastSensorEvent', 'cumulativeTime','activity']
    activities = 'sleeping'

    #read the CSV file
    df = pd.read_csv(filename)

    #cumulativeTime column created from day1 000 (equivalent to first second of first day)
    df = create_cumulativeTime_col(df)

    convert_to_timeseries(df, 60, 'cumulativeTime', 'activity')

if __name__ == "__main__":
    example_main()
