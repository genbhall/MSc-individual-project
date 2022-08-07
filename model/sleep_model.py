# from orion.evaluation.contextual import contextual_accuracy, contextual_f1_score, contextual_precision
from optparse import Values
from supporting_func.supporting_func import time_segments_aggregate, rolling_window_sequences, convert_dfdatetotime
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
    # tgan.fit(X)
    
    #notes - caught on the generator. Builds all the layers, then target shape is 500
    #error is happening in the construction of the sequential_2 layer target_shape 2 build
    
    # X_hat, critic = tgan.predict(X)
    # # flatten the predicted windows 
    
    # error, true_index, true, pred = score_anomalies(X, X_hat, critic, X_index, rec_error_type="dtw", comb="mult")
    # pred = np.array(pred).mean(axis=2)

    # # threshold to classify the high peak data points as anomolous points
    # thresh = 8
    # intervals = list()
    # i = 0
    # max_start = len(error)
    # while i < max_start:
    #     j = i
    #     start = index[i]
    #     while error[i] > thresh:
    #         i += 1
        
    #     end = index[i]
    #     if start != end:
    #         intervals.append((start, end, np.mean(error[j: i+1])))
            
    #     i += 1
            
    # anomalies = pd.DataFrame(intervals, columns=['start', 'end', 'score'])
    # print(anomalies)
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