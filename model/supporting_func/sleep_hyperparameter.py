from cmath import nan
from supporting_func.supporting_func import time_segments_aggregate, rolling_window_sequences, \
    save_model, anomalies_calc
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from config.model import hyperparameters
from orion.primitives.tadgan import TadGAN, score_anomalies
from orion.evaluation.contextual import contextual_recall, contextual_f1_score, contextual_precision

#possible options
window_szs = [100,200,400]
time_intervals = [1800,300]
epochs_range = [5,10,30,50]
latent_dims = [5,10,20]
score_windows = [5,10,50]
thresholds = [5,8,10]


#input the dataframes for training and valid test
def hyperparameter_tuning(df_train, df_valid, ground_truth):
    
    #reload from old version - line 324
    #optimal hyperparameter combination
    highest_f1 = 0.84
    highest_precision = 1.0
    highest_recall = 0.9
    log_file = open('hyperparam_logs/sleep/log_file_sleep.txt', 'a')
    
    #tracking optimal hyperparameters
    optimal_f1_combination = list()
    optimal_precision_combination = list()
    optimal_recall_combination = list()
    
    #fit the time intervals first
    for time_interval in time_intervals:

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

        #then change window_size, epochs and latent dimensions
        for window_sz in window_szs:
            
            #split into rolling window sequences - x_val_train = windows, y = without split into windows
            x_val_train, _, _, _ = rolling_window_sequences(x_val_train, index_train, 
                                                            window_size=window_sz, 
                                                            target_size=1, 
                                                            step_size=1,
                                                            target_column=0)
            
            #split into rolling window sequences - x_val_train = windows, y = without split into windows
            x_val_valid, _, values_index_valid, _ = rolling_window_sequences(x_val_valid, index_valid, 
                                                            window_size=window_sz, 
                                                            target_size=1, 
                                                            step_size=1,
                                                            target_column=0)
                                
            for epochs in epochs_range:
                for latent_dim in latent_dims:
            
                    #Train the model
                    hyperparameters["epochs"] = epochs
                    hyperparameters["input_shape"] = (window_sz, 1) # based on the window size
                    hyperparameters["target_shape"] = (window_sz, 1) # based on the window size
                    hyperparameters["optimizer"] = "keras.optimizers.Adam"
                    hyperparameters["learning_rate"] = 0.0005
                    hyperparameters["latent_dim"] = latent_dim
                    hyperparameters["batch_size"] = 64
                    hyperparameters["layers_generator"][1]["parameters"]["units"] = int(window_sz/2)
                    hyperparameters["layers_encoder"][2]["parameters"]["units"] = int(latent_dim)

                    
                    #build model and fit with data
                    tgan = TadGAN(**hyperparameters)
                    tgan.fit(x_val_train)

                    #this reconstructs the values and gives the critic score for each input sequence
                    x_val_hat_valid, critic_valid = tgan.predict(x_val_valid)
                    
                    for score_window in score_windows:
                        for threshold in thresholds:
                    
                            #anomaly scoring - score window - Size of the window over which the scores are calculated
                            error, _, _, _ = score_anomalies(x_val_valid, 
                                                            x_val_hat_valid, 
                                                            critic_valid, 
                                                            values_index_valid,
                                                            score_window=score_window,
                                                            rec_error_type="dtw", 
                                                            comb="mult")
                            
                            #calculate what counts as an anomaly based on threshold
                            intervals = anomalies_calc(threshold, error, index_valid)
                            anomalies = pd.DataFrame(intervals, columns=['start', 'end', 'score'])
                            
                            #calculate appropriate metrics - weighted = false (overlap method)
                            f1_overlap = round(contextual_f1_score(ground_truth, anomalies, df_valid, weighted=False),2)
                            precision_overlap = round(contextual_precision(ground_truth, anomalies, df_valid, weighted=False),2)
                            recall_overlap = round(contextual_recall(ground_truth, anomalies, df_valid, weighted=False),2)
                            
                            #save the best models in pickle files
                            if f1_overlap > highest_f1:
                                save_model(tgan, "sleep/f1_high_sleep.pickle")
                                highest_f1 = f1_overlap
                                optimal_f1_combination = [window_sz, time_interval, epochs, latent_dim, score_window, threshold, f1_overlap] 
                                optimal_combo = open("hyperparam_logs/sleep/optimal_combo_sleep.txt","w")
                                optimal_combo.write(f"Optimal_f1: {optimal_f1_combination} \nOptimal_prec: {optimal_precision_combination} \nOptimal_recall: {optimal_recall_combination} \n")
                                optimal_combo.close()
                            if precision_overlap > highest_precision:
                                save_model(tgan, "sleep/precision_high_sleep.pickle")
                                highest_precision = precision_overlap
                                optimal_precision_combination = [window_sz, time_interval, epochs, latent_dim, score_window, threshold, precision_overlap]
                                optimal_combo = open(f"hyperparam_logs/sleep/optimal_combo_sleep.txt","w")
                                optimal_combo.write("Optimal_f1: {optimal_f1_combination} \nOptimal_prec: {optimal_precision_combination} \nOptimal_recall: {optimal_recall_combination} \n")
                                optimal_combo.close() 
                            if recall_overlap > highest_recall:
                                save_model(tgan, "sleep/recall_high_sleep.pickle")
                                highest_recall = recall_overlap
                                optimal_recall_combination = [window_sz, time_interval, epochs, latent_dim, score_window, threshold, recall_overlap] 
                                optimal_combo = open("hyperparam_logs/sleep/optimal_combo_sleep.txt","w")
                                optimal_combo.write(f"Optimal_f1: {optimal_f1_combination} \nOptimal_prec: {optimal_precision_combination} \nOptimal_recall: {optimal_recall_combination} \n")
                                optimal_combo.close()
                                
                            #print metrics - NO ACCURACY BECAUSE NO TRUE NEGATIVES
                            print(f"Model: (wsz:{window_sz}, ti:{time_interval}, epochs:{epochs}, ld:{latent_dim}, sw:{score_window}, thresh:{threshold}) -- f1: {f1_overlap} | Precision: {precision_overlap} | recall: {recall_overlap}")
                            
                            #write output to file logs
                            log_file.write(f"\n{window_sz},{time_interval},{epochs},{latent_dim},{score_window},{threshold},{f1_overlap},{precision_overlap},{recall_overlap}")
    
    log_file.close()
    print("FINISHED!!")

#input the dataframes for training and valid test
def model_distribution_tuning(df_train, df_valid, ground_truth, iteration=10):
    
    #get the models that we're testing
    df = pd.read_csv("hyperparam_logs/sleep/F1_top_5.csv")
    model_params = df.to_numpy()

    for model_param in model_params:
        
        model_count = 1

        #set the model parameters
        window_sz = model_param[1]
        time_interval = model_param[2]
        epochs = model_param[3]
        latent_dim = model_param[4]
        score_window = model_param[5]        
        threshold = model_param[6]

        for i in range(iteration):
            
            log_file = open('hyperparam_logs/sleep/hyper_param_distribution.txt', 'a')
            
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
            x_val_train, _, _, _ = rolling_window_sequences(x_val_train, index_train, 
                                                            window_size=window_sz, 
                                                            target_size=1, 
                                                            step_size=1,
                                                            target_column=0)
            
            #split into rolling window sequences - x_val_train = windows, y = without split into windows
            x_val_valid, _, values_index_valid, _ = rolling_window_sequences(x_val_valid, index_valid, 
                                                            window_size=window_sz, 
                                                            target_size=1, 
                                                            step_size=1,
                                                            target_column=0)

            #Train the model
            hyperparameters["epochs"] = epochs
            hyperparameters["input_shape"] = (window_sz, 1) # based on the window size
            hyperparameters["target_shape"] = (window_sz, 1) # based on the window size
            hyperparameters["optimizer"] = "keras.optimizers.Adam"
            hyperparameters["learning_rate"] = 0.0005
            hyperparameters["latent_dim"] = latent_dim
            hyperparameters["batch_size"] = 64
            hyperparameters["layers_generator"][1]["parameters"]["units"] = int(window_sz/2)
            hyperparameters["layers_encoder"][2]["parameters"]["units"] = int(latent_dim)

            #build model and fit with data
            tgan = TadGAN(**hyperparameters)
            tgan.fit(x_val_train)


            #this reconstructs the values and gives the critic score for each input sequence
            x_val_hat_valid, critic_valid = tgan.predict(x_val_valid)


            #anomaly scoring - score window - Size of the window over which the scores are calculated
            error, _, _, _ = score_anomalies(x_val_valid, 
                                                            x_val_hat_valid, 
                                                            critic_valid, 
                                                            values_index_valid,
                                                            score_window=score_window,
                                                            rec_error_type="dtw", 
                                                            comb="mult")
            

            #calculate what counts as an anomaly based on threshold
            intervals = anomalies_calc(threshold, error, index_valid)
            anomalies = pd.DataFrame(intervals, columns=['start', 'end', 'score'])
            
            #calculate appropriate metrics - weighted = false (overlap method)
            f1_overlap = round(contextual_f1_score(ground_truth, anomalies, df_valid, weighted=False),2)
            precision_overlap = round(contextual_precision(ground_truth, anomalies, df_valid, weighted=False),2)
            recall_overlap = round(contextual_recall(ground_truth, anomalies, df_valid, weighted=False),2)

            #save the model parameters
            save_model(tgan, f"sleep/model_{model_count}/sleep_model_{i}.pickle")            

            #print metrics - NO ACCURACY BECAUSE NO TRUE NEGATIVES
            print(f"Model: (wsz:{window_sz}, ti:{time_interval}, epochs:{epochs}, ld:{latent_dim}, sw:{score_window}, thresh:{threshold}) -- f1: {f1_overlap} | Precision: {precision_overlap} | recall: {recall_overlap}")
            
            #write output to file logs
            log_file.write(f"\n{window_sz},{time_interval},{epochs},{latent_dim},{score_window},{threshold},{f1_overlap},{precision_overlap},{recall_overlap}")
            log_file.close()

            del x_val_train, x_val_valid, index_train, index_valid

        model_count += 1

    print("FINISHED!!")
