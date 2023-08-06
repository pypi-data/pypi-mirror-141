# TODO: This needs rework or drop
from datetime import datetime
from typing import Optional

import pandas as pd


def string_to_datetime(time_object: str) -> datetime:
    """
    Converts a string to a datetime object.

    Parameters:
        str_time (str): the string object

    Return:
        A datetime object

    """
    if time_object is not None:
        time_object = datetime.strptime(time_object, "%Y-%m-%d %H:%M:%S")

    return time_object


def get_target_from_usecase(use_case: str) -> str:
    """
    Returns the target feature name based on a use-case.

    Parameters:
        use_case (str): the use case name

    Returns:
        The targer feature name of the use case
    """

    if use_case == "UEBA: User Credentials Compromisation":
        return "related:name"


def split_dataset(data: pd.DataFrame, target_col: Optional[str]):
    """
    Extracts the data, the ids and the target from a dataset.

    Parameters:
        data (pd.DataFrame): The dataset
        target_col (Optional(str)): The name of the target columns
    """
    ids = pd.Series(dtype="str")
    target = pd.Series(dtype="str")

    if "_id" in data.columns:
        ids = data.pop("_id")
    if target_col is not None:
        if target_col in data.columns:
            target = data.pop(target_col)
        else:
            raise ValueError("Target column missing")

    return data, ids, target
