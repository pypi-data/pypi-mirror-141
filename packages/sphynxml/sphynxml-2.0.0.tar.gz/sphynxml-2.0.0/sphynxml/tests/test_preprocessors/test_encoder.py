import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from sphynxml.Preprocessors.SphynxEncoder import SphynxEncoder


def test_label_encoder_type_data_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to label_encoder()
    | THEN    A TypeError exception is raised
    """
    enc = SphynxEncoder()
    list_v = ["Athens", "Paris", "Berlin", "Athens", "Rome"]
    with pytest.raises(TypeError) as excinfo:
        enc.label_encoder(list_v)

    assert (
        str(excinfo.value) == "Expected object of type 'pd.DataFrame'  but got"
        f" {type(list_v)}"
    )


def test_label_encoder_frame():
    """
    | GIVEN   A pd.DataFrame
    | WHEN    Passing the frame to label_encoder()
    | THEN    An encoded frame is returned. Only the columns of type string are encoded.
    """
    data = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
    }
    true_res = {
        "City": [0, 2, 1, 0, 3],
        "Date": [1, 1, 0, 1, 0],
        "Year": [2020, 2020, 1990, 2020, 2021],
    }

    data = pd.DataFrame(data)
    true_res = pd.DataFrame(true_res)

    enc = SphynxEncoder()
    res = enc.label_encoder(data)

    assert_frame_equal(res, true_res)


def test_label_encoder_train_test_examples():
    """
    | GIVEN   A  pd.dataframe for training
    | A single sample for testing
    | WHEN    Calling label_encoder on both train and test frames
    | THEN    The encoder should encode both frames with the same format
    """

    data_train = {
        "City": ["Athens", "Paris", "Berlin", "Athens", "Rome"],
        "Date": ["June", "June", "July", "June", "July"],
        "Year": [2020, 2020, 1990, 2020, 2021],
    }
    data_train = pd.DataFrame(data_train)

    data_test = {"City": ["Paris", "Athens"], "Date": ["July", "June"]}
    data_test = pd.DataFrame(data_test)

    enc = SphynxEncoder()
    enc_data_train = enc.label_encoder(data_train)
    enc_data_test = enc.label_encoder(data_test)

    assert enc_data_train["City"][0] == enc_data_test["City"][1]
    assert enc_data_train["Date"][0] == enc_data_test["Date"][1]


def test_one_vs_all_encoder_type_exception():
    """
    | GIVEN   A list object of values
    | WHEN    Passing the list to one_vs_all_encoder
    | THEN    A TypeError exception is raised
    """
    enc = SphynxEncoder()
    list_v = ["Athens", "Paris", "Berlin", "Athens", "Rome"]
    with pytest.raises(TypeError) as excinfo:
        enc.one_vs_all_encoder(list_v, "Athens")

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.Series' but got {type(list_v)}"
    )


def test_one_vs_all_encoder_series():
    """
    | GIVEN   A pd.Series of string values
    | WHEN    Passing the series to one_vs_all_encoder
    | THEN    An one-hot-encoded series is returned
    """
    enc = SphynxEncoder()
    data = ["Athens", "Paris", "Berlin", "Athens", "Rome"]
    data = pd.Series(data)
    res = enc.one_vs_all_encoder(data, "Athens")

    true_res = [1, -1, -1, 1, -1]

    assert res.shape == (5,)
    assert list(res) == true_res
