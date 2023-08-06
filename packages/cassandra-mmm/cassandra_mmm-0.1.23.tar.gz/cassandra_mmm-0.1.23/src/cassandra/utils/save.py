import pandas as pd
from cassandra.model.modelEvaluation.evaluation import response_regression_to_dataset, decomposition_to_dataset


def save_metric_to_csv(metric_dictionary, path_file_to_save):
    my_dict = [metric_dictionary]
    df = pd.DataFrame.from_dict(my_dict)
    df.to_csv(path_file_to_save, index = False, header=True)

def save_timeseries_to_csv(df, name_date_column, name_target_colum, name_prediction_column, coef_dict, features, path_file_to_save):
    response_df = response_regression_to_dataset(df, name_date_column, name_target_colum, name_prediction_column, coef_dict,
                                   features)
    response_df.to_csv(path_file_to_save, index = False, header=True)

def save_decomposition_to_csv(df, coef_dict, features, path_file_to_save):
    response_df = decomposition_to_dataset(df, coef_dict, features)
    response_df.to_csv(path_file_to_save, index = False, header=True)

def save_dataset_to_csv(df, path_file_to_save):
    df.to_csv(path_file_to_save, index = False, header=True)