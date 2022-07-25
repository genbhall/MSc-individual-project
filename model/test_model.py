from orion import Orion
import pandas as pd
from output_utils.utils import plot
from supporting_func.key_variables import all_activities

if __name__ == "__main__":
    
    filename = "../preprocessing/processed_data/hh101_preprocessed_60sw.csv"
    df = pd.read_csv(filename)
    df = df[all_activities]


    orion = Orion(pipeline='config/tadgan.json')
    
    anomalies = orion.fit_detect(df)
    # plot(df,[anomalies])
    print(anomalies.head(10))

'''
from supporting_func.supporting_func import save_model, load_model
Notes: pickle - to train model, use orion.fit(df). - this will train the latent space. Then can save_model(orion)
when you load, save it as a new object. Then run orion.detect(df) to find said anomalies (as anomalies)
'''

'''
hyperparameter tuning - can set variables here

parameters = {
    "mlprimitives.custom.timeseries_preprocessing.time_segments_aggregate#1": {
        "interval": 3600 # hour level
    },
    'orion.primitives.tadgan.TadGAN#1': {
        'epochs': 15,
        'latent_dim': 40,
        'dense_units': 40,
    }
}
'''