from orion import Orion
import pandas as pd
from utils import plot

if __name__ == "__main__":
    
    filename = "../preprocessing/processed_data/hh101_preprocessed_60sw.csv"
    df = pd.read_csv(filename)
    df = df[['Time', 'Sleep']]

    orion = Orion(pipeline='tadgan.json')

    anomalies = orion.fit_detect(df)
    plot(df,[anomalies])
    print(anomalies.head(10))
