from datetime import datetime

import pandas as pd
import pytest
from pandas import testing as tm

from sphynxml.utils._SphynxETL import (
    get_target_from_usecase,
    split_dataset,
    string_to_datetime,
)


def test_string_to_datetime():
    """
    | GIVEN   A string of a date
    | WHEN    Passing the string to string_to_datetime()
    | THEN    A datetime object is returned same as the one in the string
    """

    str_date = "2022-9-10 09:34:23"
    dt_date = string_to_datetime(str_date)

    assert dt_date == datetime(2022, 9, 10, 9, 34, 23)


def test_get_target_from_usecase():
    """
    | GIVEN   The name of a available use-case in the form of a string
    | WHEN    Passing the name to get_target_from_usecase()
    | THEN    The target column name for the specified use-case is returned
    """

    uc = "UEBA: User Credentials Compromisation"
    target_name = get_target_from_usecase(uc)

    assert target_name == "related:name"


def test_split_dataset():
    """
    | GIVEN   A pd.DataFrame containing an "_id" column
    | WHEN    Passing the frame to split_dataset() with the name of the target column
    | THEN    The frame is returned split into the actual features in the form of a
    | pd.DataFrame, the ids and the target in the form of a pd.Series
    """

    data = {
        "_id": [1, 2, 3, 4, 5],
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
    }
    data = pd.DataFrame(data)
    true_ids = data["_id"]
    true_target = data["Year"]

    data_split, ids, target = split_dataset(data, "Year")

    assert data_split.shape == (5, 2)
    tm.assert_series_equal(ids, true_ids)
    tm.assert_series_equal(target, true_target)


def test_split_dataset_missing_target_exception():
    """
    | GIVEN   A pd.DataFrame
    | WHEN    Calling split_dataset with a target column name parameter that does not
    | exist in the frame's columns
    | THEN    A ValueError exception is raised
    """

    data = {
        "_id": [1, 2, 3, 4, 5],
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
    }
    data = pd.DataFrame(data)

    with pytest.raises(ValueError) as excinfo:
        split_dataset(data, "Name")

    assert str(excinfo.value) == "Target column missing"
