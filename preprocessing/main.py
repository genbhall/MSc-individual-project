import pandas as pd
import datetime
from supporting_func.preprocessing import create_cumulativeTime_col, convert_to_timeseries, add_datetime_column
from global_variables.global_variables import filename, data_name, start_date, interval

#file processes selected csv files from HH series in CASAS to binary time series of activities 

def example_main():

    #read the CSV file
    df = pd.read_csv(filename)

    #cumulativeTime column created from day1 000 (equivalent to first second of first day)
    df = create_cumulativeTime_col(df)

    ts_df = convert_to_timeseries(df, interval, 'cumulativeTime', 'activity')
    add_datetime_column(ts_df, start_date)
    ts_df.to_csv(f"processed_data/{data_name}/{data_name}_preprocessed_{interval}sw.csv")
    
if __name__ == "__main__":
    example_main()
