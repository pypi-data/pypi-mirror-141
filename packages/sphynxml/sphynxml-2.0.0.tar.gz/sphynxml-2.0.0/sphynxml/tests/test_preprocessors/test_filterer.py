import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from sphynxml.Preprocessors.SphynxFilterer import SphynxFilterer


def test_constant_features_type_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to constant_features()
    | THEN    A TypeError exception is raised
    """

    flt = SphynxFilterer()
    data = ["Athens", "Paris", "Berlin", "Athens", "Rome"]

    with pytest.raises(TypeError) as excinfo:
        flt.constant_features(data)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' but got {type(data)}"
    )


def test_constant_features_empty():
    """
    | GIVEN   A pd.DataFrame with no constant features
    | WHEN    Passing the frame to constant_features()
    | THEN    An empty list is returned
    """
    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["short", "short", "long", "long"],
    }
    data = pd.DataFrame(data)
    constant_cols = flt.constant_features(data)

    assert constant_cols == []


def test_constant_features_unique():
    """
    | GIVEN   A pd.DataFrame with one constant feature
    | WHEN    Passing the frame to constant_features()
    | THEN    A list of the column name of the constant feature is returned (single element)
    """

    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["short", "short", "long", "long"],
    }
    data = pd.DataFrame(data)
    constant_cols = flt.constant_features(data)

    assert constant_cols == ["Country"]


def test_constant_features_many():
    """
    | GIVEN   A pd.DataFrame with many constant features
    | WHEN    Passing the frame to constant_features()
    | THEN    A list of the column names of the constant features is returned
    """
    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["long", "long", "long", "long"],
    }
    data = pd.DataFrame(data)
    constant_cols = flt.constant_features(data)

    assert constant_cols == ["Country", "Hair"]


def test_cardinal_features_type_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to cardinal_features()
    | THEN    A TypeError exception is raised
    """

    flt = SphynxFilterer()
    data = ["Athens", "Paris", "Berlin", "Athens", "Rome"]

    with pytest.raises(TypeError) as excinfo:
        flt.cardinal_features(data)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' but got {type(data)}"
    )


def test_cardinal_features_empty():
    """
    | GIVEN   A pd.DataFrame with no cardinal features
    | WHEN    Passing the frame to cardinal_features()
    | THEN    An empty list is returned
    """

    flt = SphynxFilterer()
    data = {
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["short", "short", "long", "long"],
    }
    data = pd.DataFrame(data)
    cardinal_cols = flt.cardinal_features(data)

    assert cardinal_cols == []


def test_cardinal_features_unique():
    """
    | GIVEN   A pd.DataFrame with one cardinal feature
    | WHEN    Passing the frame to cardinal_features()
    | THEN    A list of the column name of the cardinal feature is returned (single element)
    """

    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["short", "short", "long", "long"],
    }
    data = pd.DataFrame(data)
    cardinal_cols = flt.cardinal_features(data)

    assert cardinal_cols == ["Name"]


def test_cardinal_features_many():
    """
    | GIVEN   A pd.DataFrame with many cardinal features
    | WHEN    Passing the frame to cardinal_features()
    | THEN    A list of the column names of the cardinal features is returned
    """

    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["long", "long", "long", "long"],
    }
    data = pd.DataFrame(data)
    cardinal_cols = flt.cardinal_features(data)

    assert cardinal_cols == ["Name"]


def test_collinear_features_type_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to collinear_features()
    | THEN    A TypeError exception is raised
    """

    flt = SphynxFilterer()
    data = ["Athens", "Paris", "Berlin", "Athens", "Rome"]

    with pytest.raises(TypeError) as excinfo:
        flt.collinear_features(data)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' but got {type(data)}"
    )


def test_collinear_features_empty():
    """
    | GIVEN   A pd.DataFrame with no collinear features
    | WHEN    Passing the frame to collinear_features()
    | THEN    An empty list is returned
    """

    flt = SphynxFilterer()
    data = {"Country": ["Greece"] * 100, "Gender": ["male"] * 50 + ["female"] * 50}
    data = pd.DataFrame(data)
    cardinal_cols = flt.collinear_features(data)

    assert cardinal_cols == []


def test_collinear_features_unique():
    """
    | GIVEN   A pd.DataFrame with one collinear feature
    | WHEN    Passing the frame to collinear_features()
    | THEN    A list of the column name of the collinear feature is returned (single element)
    """

    flt = SphynxFilterer()
    data = {
        "Country": ["Greece"] * 100,
        "Gender": ["male"] * 50 + ["female"] * 50,
        "Hair": ["short"] * 50 + ["long"] * 50,
    }
    data = pd.DataFrame(data)
    cardinal_cols = flt.collinear_features(data)

    assert cardinal_cols == ["Gender"]


def test_data_filter_type_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to data_filter()
    | THEN    A TypeError exception is raised
    """

    flt = SphynxFilterer()
    data = ["Athens", "Paris", "Berlin", "Athens", "Rome"]

    with pytest.raises(TypeError) as excinfo:
        flt.data_filter(data)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' but got {type(data)}"
    )


def test_data_filter():
    """
    | GIVEN   A pd.DataFrame containing constant and cardinal features
    | WHEN    Passing the frame to data_filter()
    | THEN    A filtered framed is returned with no constant or cardinal features
    """

    flt = SphynxFilterer()
    data = {
        "Name": ["Andrew", "Iordanis", "Jane", "Mary"],
        "Country": ["Greece", "Greece", "Greece", "Greece"],
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["sort", "sort", "long", "long"],
    }
    res = {
        "Gender": ["male", "male", "female", "female"],
        "Hair": ["sort", "sort", "long", "long"],
    }
    data = pd.DataFrame(data)
    res = pd.DataFrame(res)
    filtered_data = flt.data_filter(data)

    assert_frame_equal(filtered_data, res)
