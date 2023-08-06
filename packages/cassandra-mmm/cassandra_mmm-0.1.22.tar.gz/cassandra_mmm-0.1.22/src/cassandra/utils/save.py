import pandas as pd

def save_metric(metric_dictionary, path_file_to_save):
    my_dict = [metric_dictionary]
    df = pd.DataFrame.from_dict(my_dict)
    df.to_csv(path_file_to_save, index = False, header=True)