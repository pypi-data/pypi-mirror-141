import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from sphynxml.Preprocessors.SphynxTransformer import SphynxTransformer


def test_type_data_exception():
    """
    | GIVEN   A dictionary
    | WHEN    Passing the dictionary to expand_timestamp()
    | THEN    A TypeError exception is raised
    """

    trf = SphynxTransformer()
    data = {"timestamp": ["2021-09-20T09:36:34.000-04:00"]}
    with pytest.raises(TypeError) as excinfo:
        trf.expand_timestamp(data, "timestamp")

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' or 'pd.Series' but got {type(data)}"
    )


def test_timestamp_name_type_exception():
    """
    | GIVEN   A pd.DataFrame with a timestamp column
    | WHEN    Passing the frame and a non-string type object as a name to expand_timestamp()
    | THEN    A TypeError exception is raised
    """

    trf = SphynxTransformer()
    data = {"timestamp": ["2021-09-20T09:36:34.000-04:00"]}
    data = pd.DataFrame(data)
    with pytest.raises(TypeError) as excinfo:
        trf.expand_timestamp(data, 5)

    assert str(excinfo.value) == f"Expected object of type 'str' but got {type(5)}"


def test_invalid_timestamp_name_exception():
    """
    | GIVEN   A pd.DataFrame with a timestamp column
    | WHEN    Passing the frame and a wrong timestamp name to expand_timestamp()
    | THEN    A ValueError exception is raised
    """

    trf = SphynxTransformer()
    data = {"timestamp": ["2021-09-20T09:36:34.000-04:00"]}
    data = pd.DataFrame(data)
    with pytest.raises(ValueError) as excinfo:
        trf.expand_timestamp(data, "timestamp_wrong")

    assert str(excinfo.value) == "Timestamp column is missing from DataFrame"


def test_invalid_timestamp_format():
    """
    | GIVEN   A pd.DataFrame with a timestamp column
    | WHEN    The format of the timestamp is not correct
    | THEN    A ValueError exception is raised
    """

    trf = SphynxTransformer()
    data = {"timestamp": ["2021-09-20T09-36-34.000-04-00"]}
    data = pd.DataFrame(data)
    with pytest.raises(ValueError) as excinfo:
        trf.expand_timestamp(data, "timestamp")

    assert str(excinfo.value) == "Invalid timestamp format"


def test_expand_timestamp_unique():
    """
    | GIVEN   A pd.DataFrame with a timestamp column containing one element
    | WHEN    Passing the frame to expand_timestamp()
    | THEN    A frame containing three features (month, day and hour) and one sample is returned
    """

    trf = SphynxTransformer()
    data = {"timestamp": ["2021-09-20T09:36:34.000-04:00"]}
    data = pd.DataFrame(data)
    res = trf.expand_timestamp(data, "timestamp")

    assert len(res.columns) == 3
    assert "month" in res.columns
    assert "day" in res.columns
    assert "hour" in res.columns
    assert res["month"][0] == "09"
    assert res["day"][0] == "20"
    assert res["hour"][0] == "09"


def test_expand_timestamp_series():
    """
    | GIVEN   A pd.Series containing one timestamp element
    | WHEN    Passing the series to expand_timestamp()
    | THEN    A frame containing three features (month, day and hour) and one sample is returned
    """

    trf = SphynxTransformer()
    data = ["2021-09-20T09:36:34.000-04:00"]
    data = pd.Series(data, name="timestamp")

    res = trf.expand_timestamp(data)

    assert len(res.columns) == 3
    assert "month" in res.columns
    assert "day" in res.columns
    assert "hour" in res.columns
    assert res["month"][0] == "09"
    assert res["day"][0] == "20"
    assert res["hour"][0] == "09"


def test_drop_list_func():
    """
    | GIVEN   A pd.DataFrame with columns of type 'list'
    | WHEN    Passing the frame to drop_list_columns
    | THEN    A frame with no columns of type 'list' is returned
    """

    trf = SphynxTransformer()
    data = {
        "Year": [2021, 2020, 1990, 2000],
        "Traveled": [["Greece", "Italy"], ["America", "Canada"], ["Japan"], ["Russia"]],
        "Cities": [["Athens", "Rome"], ["New York", "Calgary"], ["Tokyo"], ["Moscow"]],
    }
    res = {"Year": [2021, 2020, 1990, 2000]}

    data = pd.DataFrame(data)
    res = pd.DataFrame(res)
    data = trf.drop_list_columns(data)

    assert_frame_equal(data, res)
