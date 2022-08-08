# from orion.evaluation.contextual import contextual_accuracy, contextual_f1_score, contextual_precision
from supporting_func.supporting_func import time_segments_aggregate, rolling_window_sequences, \
    save_model, load_model, collapse_ts, anomalies_calc, split_data, convert_dfdatetotime
from global_variables.global_variables import filename_train, all_activities, filename_test, filename_summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from orion.primitives.tadgan import TadGAN, score_anomalies
from config.model import hyperparameters
from orion.evaluation.contextual import contextual_accuracy, contextual_recall, contextual_f1_score, contextual_precision

if __name__ == "__main__":
    
    #read and split the relevant files
    df = pd.read_csv(filename_test)
    ground_truth = pd.read_csv(filename_summary)
    df_split = split_data(df, 30)
    df_train = df_split[0][all_activities]
    df_valid = df_split[1][all_activities]

    #hyperparameters    
    time_interval = 300 #in seconds - for data (fine tune?)
    window_sz = 200
    
    #breakout the df into numpy arrays for training
    x_val_train, index_train = time_segments_aggregate(df_train, 
                                              interval=time_interval)
    
    #breakout the df into numpy arrays for validation
    x_val_valid, index_valid = time_segments_aggregate(df_valid, 
                                              interval=time_interval)
    
    #scale everything from -1 to 1 using sklearn package
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x_val_train = scaler.fit_transform(x_val_train)
    x_val_valid = scaler.fit_transform(x_val_valid)
    
    #split into rolling window sequences - x_val_train = windows, y = without split into windows
    x_val_train, y_train, values_index_train, y_index_train = rolling_window_sequences(x_val_train, index_train, 
                                                    window_size=window_sz, 
                                                    target_size=1, 
                                                    step_size=1,
                                                    target_column=0)
    
    #split into rolling window sequences - x_val_train = windows, y = without split into windows
    x_val_valid, y_valid, values_index_valid, y_index_valid = rolling_window_sequences(x_val_valid, x_index_valid, 
                                                    window_size=window_sz, 
                                                    target_size=1, 
                                                    step_size=1,
                                                    target_column=0)
    
    #Train the model
    hyperparameters["epochs"] = 10
    hyperparameters["input_shape"] = (window_sz, 1) # based on the window size
    hyperparameters["target_shape"] = (window_sz, 1) # based on the window size
    hyperparameters["optimizer"] = "keras.optimizers.Adam"
    hyperparameters["learning_rate"] = 0.0005
    hyperparameters["latent_dim"] = 20
    hyperparameters["batch_size"] = 64
    hyperparameters["layers_generator"][1]["parameters"]["units"] = int(window_sz/2)

    #build model and fit with data - then save.
    tgan = TadGAN(**hyperparameters)
    tgan.fit(x_val_train)
    save_model(tgan, "sleep_tgan.pickle")
   
    #this reconstructs the values and gives the critic score for each input sequence
    x_val_hat_valid, critic_valid = tgan.predict(x_val_valid)

    # #not needed for .py run but helpful in understanding how this works
    # y_hat = collapse_ts(x_values_hat)
    

    #anomaly scoring - score window - Size of the window over which the scores are calculated
    error, true_index, true, pred = score_anomalies(x_val_valid, 
                                                    x_val_hat_valid, 
                                                    critic_valid, 
                                                    values_index_valid,
                                                    score_window=10,
                                                    rec_error_type="dtw", 
                                                    comb="mult")
    
    pred = np.array(pred).mean(axis=2)

    # ge the threshold to classify the high peak data points as anomolous points
    threshold = 5
    intervals = anomalies_calc(threshold, error, index_valid)
    anomalies = pd.DataFrame(intervals, columns=['start', 'end', 'score'])
            
    #prepare the relevant ground truth file
    ground_truth = pd.read_csv(filename_summary)
    ground_truth = convert_dfdatetotime(ground_truth)

    #calculate appropriate metrics - weighted = false
    f1_overlap = contextual_f1_score(ground_truth, anomalies, df_valid, weighted=False)
    precision_overlap = contextual_precision(ground_truth, anomalies, df_valid, weighted=False)
    recall_overlap = contextual_recall(ground_truth, anomalies, df_valid, weighted=False)
    accuracy_overlap = contextual_accuracy(ground_truth, anomalies, df_valid, weighted=False)
    
    #save all settings and scores, then append to file.txt with outputs