from orion import Orion
import pandas as pd
from output_utils.utils import plot
from supporting_func.supporting_func import split_data, save_model, load_model, print_anomalies
from global_variables.global_variables import filename_train, all_activities, filename_test

if __name__ == "__main__":
    
    pickle_file = "sleep_model.pickle"


    # dict_dfs = split_data(df,30)
    # training_df = dict_dfs[0][all_activities]
    # test_df = dict_dfs[1][all_activities]

    # df = pd.read_csv(filename_train)
    # df = df[all_activities]
    # orion = Orion(pipeline='config/tadgan.json')
    # orion.fit(df)
    # save_model(orion, pickle_file)

    df = pd.read_csv(filename_test)
    df = df[all_activities]
    orion = load_model(pickle_file)
    anomalies = orion.detect(df)
    anomalies = pd.DataFrame(anomalies)
    print(anomalies)
    print_anomalies(anomalies, filename_test)
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