import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from sphynxml.utils._preprocessor import split_data_target


def test_split_data_target():
    """
    | GIVEN   A pd.DataFrame
    | WHEN    Calling split_data_target() with tha data and the name of the target column
    | THEN    The dataset is returned split into a pd.DataFrame with the features and a
    | pd.Series with the target column
    """

    data = {"height": [1.80, 1.65, 1.70], "weight": [75, 60, 70], "age": [20, 14, 27]}
    data = pd.DataFrame(data)

    new_data, target = split_data_target(data, "age")

    assert_series_equal(data["age"], target)
    assert_frame_equal(data[["height", "weight"]], new_data)
