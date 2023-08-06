import pandas as pd
import pytest
from numpy import NaN

from sphynxml.Statistics.Statistics import InfoStats


def test_get_nan_percentage_type_exception():
    """
    | GIVEN   A non pd.Series or pd.DataFrame object
    | WHEN    Calling the get_nan_percentage()
    | THEN    A TypeError exception is raised
    """

    infs = InfoStats()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        infs.get_nan_percentage(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_nan_percentage_empty():
    """
    | GIVEN   An empty pd.DataFrame
    | WHEN    Calling the get_nan_percentage
    | THEN    The % of NaN should be zero
    """

    infs = InfoStats()

    df = pd.DataFrame(columns=["Name", "Country", "Gender"])
    res = infs.get_nan_percentage(df)

    assert res.sum() == 0


def test_get_nan_percentage():
    """
    | GIVEN   A pd.DataFrame with some percentage of NaN values
    | WHEN    Calling the get_nan_percentage
    | THEN    A % value for each columns is returned, representing the percentage
    | of NaN values in the respective column
    """

    infs = InfoStats()
    data = {
        "City": [NaN, "Paris", NaN, NaN, "Rome"],
        "Date": ["June", NaN, NaN, "June", "July"],
        "Year": [2020, 2020, NaN, 2020, NaN],
    }
    data = pd.DataFrame(data)
    res = infs.get_nan_percentage(data)

    assert res["City"] == 60
    assert res["Date"] == 40
    assert res["Year"] == 40


def test_get_info_stats_type_exception():
    """
    | GIVEN   A non pd.Series or pd.DataFrame object
    | WHEN    Calling the get_info_stats()
    | THEN    A TypeError exception is raised
    """

    infs = InfoStats()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        infs.get_info_stats(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_info_stats():
    """
    | GIVEN   A pd.DataFrame
    | WHEN    Calling the get_info_stats()
    | THEN    A pd.DataFrame is returned with general information about the dataset
    """

    infs = InfoStats()
    data = {
        "City": [NaN, "Paris", NaN, NaN, "Rome"],
        "Date": ["June", NaN, NaN, "June", "July"],
        "Year": [2020, 2020, NaN, 2020, NaN],
    }
    data = pd.DataFrame(data)
    res = infs.get_info_stats(data)

    assert res.shape == (3, 3)
