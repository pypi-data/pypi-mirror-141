import pandas as pd
import pytest
from numpy import NaN

from sphynxml.Statistics.Statistics import SummaryStatistics


def test_get_mode_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_mode()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_mode(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_mode():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_mode
    THEN    A DataFrame with the mode of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_mode(data)

    assert res.shape == (1, 4)
    assert res["City"][0] == "Athens"
    assert res["Date"][0] == "June"
    assert res["Year"][0] == 2020
    assert res["Age"][0] == 19


def test_get_mean_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_mean()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_mean(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_mean():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_mean
    THEN    A DataFrame with the mean value of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_mean(data)

    assert res.shape == (2,)
    assert res["Year"] == 2014.2
    assert res["Age"] == 19.6


def test_get_median_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_median()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_median(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_median():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_median
    THEN    A DataFrame with the median value of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_median(data)

    assert res.shape == (2,)
    assert res["Year"] == 2020
    assert res["Age"] == 19


def test_get_max_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_max()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_max(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_max():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_max
    THEN    A DataFrame with the maximum value of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_max(data)

    assert res.shape == (4,)
    assert res["City"] == "Rome"
    assert res["Date"] == "June"
    assert res["Year"] == 2021
    assert res["Age"] == 30


def test_get_min_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_min()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_min(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_min():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_min
    THEN    A DataFrame with the minimum value of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_min(data)

    assert res.shape == (4,)
    assert res["City"] == "Athens"
    assert res["Date"] == "July"
    assert res["Year"] == 1990
    assert res["Age"] == 10


def test_get_std_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_std()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_std(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_std():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_std
    THEN    A DataFrame with the standard deviation of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_std(data)

    assert res.shape == (2,)
    assert res["Year"].round(2) == 13.54
    assert res["Age"].round(2) == 7.09


def test_get_quantile_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_quantile()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_quantile(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_quantile_50():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_quantile
    THEN    A DataFrame with the 50-quantile of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_quantile(data)

    assert res.shape == (2,)
    assert res["Year"].round(2) == 2020
    assert res["Age"].round(2) == 19


def test_get_quantile_20():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_quantile with q parameter initialized to .2
    THEN    A DataFrame with the 20-quantiles of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_quantile(data, q=0.20)

    assert res.shape == (2,)
    assert res["Year"].round(2) == 2014
    assert res["Age"].round(2) == 17.2


def test_get_summary_stats_type_exception():
    """
    GIVEN   A non pd.Series or pd.DataFrame type object
    WHEN    Calling get_summary_stats()
    THEN    A TypeError exception is raised
    """

    ss = SummaryStatistics()
    data_list = {"City": [NaN, "Paris", NaN, NaN, "Rome"]}
    with pytest.raises(TypeError) as excinfo:
        ss.get_summary_stats(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_get_summary_stats():
    """
    GIVEN   A pd.DataFrame
    WHEN    Calling get_summary_stats
    THEN    A DataFrame with the summary statistics of each column is returned
    """

    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    ss = SummaryStatistics()

    res = ss.get_summary_stats(data)

    assert res.shape == (11, 4)
