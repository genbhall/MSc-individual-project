from orion import Orion
from orion.evaluation.contextual import contextual_accuracy, contextual_f1_score, contextual_precision
import pandas as pd
from output_utils.utils import plot
from supporting_func.supporting_func import split_data, save_model, load_model, print_anomalies, convert_dfdatetotime, convert_dftimetodate
from global_variables.global_variables import filename_train, all_activities, filename_test, filename_summary

if __name__ == "__main__":
    
    pickle_file = "sleep_model.pickle"

    df = pd.read_csv(filename_train)
    dict_dfs = split_data(df,30)
    training_df = dict_dfs[0][all_activities]
    test_df = dict_dfs[1][all_activities]

    test_df = test_df[all_activities]
    parameters = {
        "mlprimitives.custom.timeseries_preprocessing.time_segments_aggregate#1": {
            "interval": 300 # 5min
        },
        'orion.primitives.tadgan.TadGAN#1': {
            'epochs': 20,
            'latent_dim': 50,
            'dense_units': 50,
        }
    }
    orion = Orion(pipeline='config/tadgan.json', hyperparameters=parameters)
    orion.fit(test_df)
    save_model(orion, pickle_file)

    # # load and read files - detect anomalies
    # df = pd.read_csv(filename_test)
    # df = df[all_activities]
    # orion = load_model(pickle_file)
    # prediction = orion.predict(test_df)
    # print(prediction)
    # # anomalies, visualise = orion.detect(df, visualization=True)
    # print(anomalies)
    # print(visualise)

    # # evaluate the anomalies 
    # ground_truth = pd.read_csv(filename_summary)
    # print(ground_truth)
    # ground_truth = convert_dfdatetotime(ground_truth)
    # metrics = [
    #     'f1',
    #     'recall',
    #     'precision',
    # ]
    # scores = orion.evaluate(df, ground_truth, fit=False, metrics=metrics)
    # print(scores)

    # # anomalies = convert_dftimetodate(anomalies)
    # print(anomalies)
    # print_anomalies(anomalies, filename_test)
    # plot(df,[anomalies])
    # print(anomalies.head(10))

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