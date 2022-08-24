from supporting_func.supporting_func import split_data, convert_dfdatetotime
from global_variables.global_variables import all_activities, filename_test, filename_summary
from supporting_func.sleep_hyperparameter import hyperparameter_tuning, model_distribution_tuning, final_distribution_tuning

import pandas as pd

if __name__ == "__main__":
    
    print(filename_test)
    print(filename_summary)
    
    #read and split the relevant files
    df = pd.read_csv(filename_test)
    ground_truth = pd.read_csv(filename_summary)
    df_split = split_data(df, 30)
    df_train = df_split[0][all_activities]
    df_valid = df_split[1][all_activities]

    #prepare the relevant ground truth file
    ground_truth = convert_dfdatetotime(ground_truth)
    
    #hyperparameter tuning
    # hyperparameter_tuning(df_train, df_valid, ground_truth)
    
    # # This is saved
    # #test for distributions of top 5 models - saves outcomes in new file
    # top_5_params = pd.read_csv("hyperparam_logs/sleep/F1_top_5.csv")
    # model_distribution_tuning(df_train, df_valid, top_5_params, ground_truth)
    
    #FINAL TEST FOR EVALUATION PURPOSES ON HH120
    final_model_param = ['',100,1800,10,20,5,5]
    final_distribution_tuning(df_train, df_valid, final_model_param, ground_truth)