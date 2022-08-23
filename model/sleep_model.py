from supporting_func.supporting_func import split_data, convert_dfdatetotime
from global_variables.global_variables import all_activities, filename_test, filename_summary
from supporting_func.sleep_hyperparameter import hyperparameter_tuning, model_distribution_tuning

import pandas as pd

if __name__ == "__main__":
    
    #read and split the relevant files
    df = pd.read_csv(filename_test)
    ground_truth = pd.read_csv(filename_summary)
    df_split = split_data(df, 30)
    df_train = df_split[0][all_activities]
    df_valid = df_split[1][all_activities]

    #prepare the relevant ground truth file
    ground_truth = convert_dfdatetotime(ground_truth)
    
    #hyperparameter tuning
    hyperparameter_tuning(df_train, df_valid, ground_truth)
    
    #test for distributions of top 5 models - saves outcomes in new file
    # model_distribution_tuning(df_train, df_valid, ground_truth)
    