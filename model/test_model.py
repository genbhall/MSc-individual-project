from orion import Orion
import pandas as pd
from output_utils.utils import plot
from supporting_func.key_variables import all_activities
from supporting_func.supporting_func import split_data, save_model, load_model, print_anomalies

if __name__ == "__main__":
    
    filename = "../preprocessing/processed_data/hh101/hh101_preprocessed_60sw.csv"
    df = pd.read_csv(filename)
    dict_dfs = split_data(df,30)

    training_df = dict_dfs[0][all_activities]
    test_df = dict_dfs[1][all_activities]


    orion = Orion(pipeline='config/tadgan.json')
    # # orion.fit(training_df)
    # # save_model(orion)

    # orion = load_model()
    # anomalies = orion.detect(test_df)
    
    # anomalies = {
    #     'start': [3070080, 5132700],
    #     'end': [3095340, 5153880],
    #     'severity': [1.44, 0.668255],
    # }


    anomalies = pd.DataFrame(anomalies)
    print(anomalies)
    print_anomalies(anomalies, filename)
    # plot(df,[anomalies])
    # print(anomalies.head(10))

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