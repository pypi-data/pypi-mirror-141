def split_data_target(data, target_name):
    """Extract the target variable from the train/test datasets and return the results

    Args:
        merged_data (pd.DataFrame): training dataframe
        target_variable (str): target variable name

    Returns:
        data (pd.DataFrame): training data without the target variable
        target (pd.Series): training target variable
    """

    target = data[target_name]
    data = data.drop(columns=[target_name], axis=1)

    return data, target
