import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#plots timeseries of indidual activities (binary signal) 
def plot_single_variable(df, time_t, variable):

    time_t = df[time_t].to_numpy()
    activity = df[variable].to_numpy()

    plt.plot(time_t, activity)
    plt.title('Time Series of {activity}')
    plt.xlabel('Time')
    plt.ylabel('{Activity}')
    plt.show()

if __name__ == "__main__":

    #target variables (to change if necessary)
    filename = "processed_data/hh101_preprocessed_60sw.csv"

    #read the CSV file
    df = pd.read_csv(filename)
    print(df.columns)

    plot_single_variable(df, 'Time', 'Sleep')