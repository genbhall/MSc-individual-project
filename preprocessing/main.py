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

    #window_60s
    ts_df = convert_to_timeseries(df, 60, 'cumulativeTime', 'activity')

    ts_df.to_csv("processed_data/hh101_preprocessed_60sw.csv")

if __name__ == "__main__":
    example_main()
