# from orion.evaluation.contextual import contextual_accuracy, contextual_f1_score, contextual_precision
from optparse import Values
from supporting_func.supporting_func import time_segments_aggregate, rolling_window_sequences, save_model, load_model, collapse_ts, anomalies_calc
from global_variables.global_variables import filename_train, all_activities, filename_test, filename_summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from orion.primitives.tadgan import TadGAN, score_anomalies
from config.model import hyperparameters
from orion.evaluation.contextual import contextual_accuracy, contextual_f1_score, contextual_precision

if __name__ == "__main__":
    
    #read the file
    df = pd.read_csv(filename_test)
    df = df[all_activities]
    
    
    
    window_sz = 200
    #here df is the given dataframe and "timestamp" is the required column to be altered.
    x_values, index = time_segments_aggregate(df, 
                                              interval=300, 
                                              time_column='timestamp')
    
    #scale everything from -1 to 1 using sklearn package
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x_values = scaler.fit_transform(x_values)
    
    #the target value; the value at time t.
    #previous observed values, this is determined by the window width.
    x_values, y, values_index, y_index = rolling_window_sequences(x_values, index, 
                                                    window_size=window_sz, 
                                                    target_size=1, 
                                                    step_size=1,
                                                    target_column=0)
    
        
    # hyperparameters["epochs"] = 10
    # hyperparameters["input_shape"] = (window_sz, 1) # based on the window size
    # hyperparameters["target_shape"] = (window_sz, 1) # based on the window size
    # hyperparameters["optimizer"] = "keras.optimizers.Adam"
    # hyperparameters["learning_rate"] = 0.0005
    # hyperparameters["latent_dim"] = 20
    # hyperparameters["batch_size"] = 64
    # hyperparameters["layers_generator"][1]["parameters"]["units"] = int(window_sz/2)

    # tgan = TadGAN(**hyperparameters)
    # tgan.fit(x_values)
    
    # save_model(tgan, "sleep_tgan.pickle")
    
    tgan = load_model("sleep_tgan.pickle")    
    
    #this reconstructs the values and gives the critic score for each input sequence
    x_values_hat, critic = tgan.predict(x_values)
  
    #not needed for .py run but helpful in understanding how this works
    y_hat = collapse_ts(x_values_hat)
    
    #anomaly scoring - score window - Size of the window over which the scores are calculated
    error, true_index, true, pred = score_anomalies(x_values, 
                                                    x_values_hat, 
                                                    critic, 
                                                    values_index,
                                                    score_window=10,
                                                    rec_error_type="dtw", 
                                                    comb="mult")
    
    pred = np.array(pred).mean(axis=2)

    # # threshold to classify the high peak data points as anomolous points
    threshold = 5
    intervals = anomalies_calc(threshold, error, index)
    anomalies = pd.DataFrame(intervals, columns=['start', 'end', 'score'])
    print(anomalies)
            
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