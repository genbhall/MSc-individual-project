import pandas as pd
from preprocessing import create_cumulativeTime_col, convert_to_timeseries

#file processes selected csv files from HH series in CASAS to binary time series of activities 

def example_main():

    #target variables (to change if necessary)
    filename = "../CASAS_dataset/23_HH101/hh101.ann.features.csv"

    #read the CSV file
    df = pd.read_csv(filename)

    #cumulativeTime column created from day1 000 (equivalent to first second of first day)
    df = create_cumulativeTime_col(df)

    window_period = 1800

    #window_1800s
    ts_df = convert_to_timeseries(df, window_period, 'cumulativeTime', 'activity')

    ts_df.to_csv("processed_data/hh101_preprocessed_1800sw.csv")

if __name__ == "__main__":
    example_main()
