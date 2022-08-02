import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from global_variables.global_variables import filename_proc


#plots timeseries of indidual activities (binary signal) 
def plot_single_variable(df, time_t, variable):

    time_t = df[time_t].to_numpy()
    activity = df[variable].to_numpy()

    plt.plot(time_t, activity)
    plt.title('Time Series of {activity}')
    plt.xlabel('timestamp')
    plt.ylabel('{Activity}')
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv(filename_proc)
    print(df.columns)
    plot_single_variable(df, 'timestamp', 'Sleep')