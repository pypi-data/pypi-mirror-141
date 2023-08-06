"""
Performs all the pre-processing transformations.

The module can extract month, day and hour values from timestamps with format
same with the one in elastic. Also, it can transform lists of objects to string
type. By using the data_transform() method the user can choose to apply
all the available data transformation methods and drop the detected features.

"""

from typing import Optional, Union

import pandas as pd

from sphynxml.BaseModeler import BaseModeler
from sphynxml.Preprocessors.tests.preprocessor_tests import check_timestamp_format


class SphynxTransformer(BaseModeler):
    """Performs pre-processing transformations."""

    def __init__(self) -> None:
        return

    def expand_timestamp(
        self,
        df: Union[pd.Series, pd.DataFrame],
        timestamp_col_name: Optional[str] = "timestamp",
    ) -> pd.DataFrame:
        """Performs feature extraction on the timestamp feature column by
        extracting the month, the day and the hour values. The timestamp must
        have the following form:
        "year-month-dayThours:minutes:seconds.000-timezone".

        Parameters:
            df (pd.DataFrame): The dataset
            timestamp_col_name: The column name of the timestamp feature

        Returns:
            A feature engineered dataframe with 3 new features ['month', 'day', 'hour']
            and with the initial timestamp feature dropped.

        Examples:
            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.Transformer import Transformer
            >>> data = {'timestamp': ['2021-09-20T09:36:34.000-04:00',
            ... '2021-08-20T09:36:34.000-04:00', '2021-07-20T09:36:34.000-04:00',
            ... '2021-04-20T09:36:34.000-04:00']}
            >>> df = pd.DataFrame(data)
            >>> trf = Transformer()
            >>> res = trf.expand_timestamp(df, 'timestamp')

            >>> res
              month day hour
            0    09  20   09
            1    08  20   09
            2    07  20   09
            3    04  20   09

        """

        if not isinstance(df, pd.DataFrame) and not isinstance(df, pd.Series):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(df)}"
            )

        if not isinstance(timestamp_col_name, str):
            raise TypeError(
                f"Expected object of type 'str' but got {type(timestamp_col_name)}"
            )

        if isinstance(df, pd.DataFrame):
            if timestamp_col_name not in df.columns:
                raise ValueError("Timestamp column is missing from DataFrame")

            if not all(df[timestamp_col_name].apply(check_timestamp_format)):
                raise ValueError("Invalid timestamp format")

        if isinstance(df, pd.DataFrame):
            ts = df[timestamp_col_name]
        else:
            ts = df

        ts = ts.str.split("T", expand=True)

        date = ts[0].str.split("-", expand=True)
        date.columns = ["year", "month", "day"]

        time = ts[1].str.split(":", expand=True)
        time.columns = ["hour", "minutes", "seconds", "zeros"]

        temp = pd.concat([date, time], axis=1)

        df = pd.concat([df, temp], axis=1)
        df = df.drop(
            columns=["seconds", "zeros", timestamp_col_name, "minutes", "year"]
        )

        return df

    def drop_list_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops columns that contain objects of type List.

        Parameters:
            df (pd.DataFrame): The dataset

        Returns:
            A filtered DataFrame with no columns with objects of type List.

        Examples:
        >>> import pandas as pd
        >>> from sphynxml.Preprocessors.SphynxTransformer import SphynxTransformer
        >>> data = {
        ...  "Year": [2021, 2020, 1990, 2000],
        ...  "Traveled": [["Greece", "Italy"], ["America", "Canada"], ["Japan"], ["Russia"]],
        ...  "Cities": [["Athens", "Rome"], ["New York", "Calgary"], ["Tokyo"], ["Moscow"]],
        ...  }
        >>> data = pd.DataFrame(data)
        >>> trf = SphynxTransformer()
        >>> data_transformed = trf.drop_list_columns(data)
        Dropped list dtype column: Traveled
        Dropped list dtype column: Cities
        >>> data_transformed
        Year
        0  2021
        1  2020
        2  1990
        3  2000

        """

        for col in df.columns:
            try:
                if all(df[col].str.contains(r"\[*\]", regex=True)):
                    print(f"Dropped list dtype column: {col}")
                    df.pop(col)
            except Exception as e:
                print(f"{e.__class__} Exception occured")
                continue

        return df
