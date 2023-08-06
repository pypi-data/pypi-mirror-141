"""
Performs the pre-processing encodings.

The module can perform data encoding and one-vs-all encoding.
"""

from typing import Union

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from sphynxml.BaseModeler import BaseModeler


class SphynxEncoder(BaseModeler):
    """Performs pre-processing encoding."""

    def __init__(self) -> None:
        self.le = LabelEncoder()
        self.label_map = {}

    # def series_label_encoder(self, series)

    # datset_label_encoder
    def label_encoder(self, data: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Encoder for transforming features of type 'object' to categorical.

        Parameters:
            df (pd.DataFrame): The data to apply the transformation

        Returns:
            A dataframe with encoded features

        Example:
            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.Encoder import Encoder
            >>> data = {'Name': ['Andreas', 'Iordanis', 'Jane', 'Mary'],
            ... 'Gender': ['male','male','female','female'], 'Age': [23, 27, 30, 28]}
            >>> df = pd.DataFrame(data)
            >>> enc = Encoder()
            >>> res = enc.data_encode(df)

            >>> res
               Name  Gender  Age
            0     0       1   23
            1     1       1   27
            2     3       0   30
            3     2       0   28

        """

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame'  but got" f" {type(data)}"
            )

        cat_f = data.columns[data.dtypes == object]
        if not self.label_map:
            for x in cat_f:
                self.le.fit(data[x])
                self.label_map[x] = dict(
                    zip(self.le.classes_, self.le.transform(self.le.classes_))
                )

        for x in cat_f:
            res = data[x].map(self.label_map[x])
            data[x] = pd.Series(res)

        return data

    def one_vs_all_encoder(self, series: pd.Series, name: str) -> pd.Series:
        """
        Performs one-vs-all encoding. Entries of the series with value equal to the
        name parameter will be encoded as '1' and the rest of the entries as '-1'.

        Parameters:
            series (pd.Series): The series to be encoded
            name (str): The value of the series to encode as '1'

        Returns:
            A binary encoded series

        Example:

            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.Encoder import Encoder
            >>> data = {'Name': ['Andreas', 'Iordanis', 'Jane', 'Mary'],
            ... 'Gender': ['male','male','female','female'], 'Age': [23, 27, 30, 28]}
            >>> df = pd.DataFrame(data)
            >>> enc = Encoder()
            >>> df['Name'] = enc.one_vs_all(df['Name'], 'Andreas')

            >>> df
                   Name  Gender  Age
            0         1    male   23
            1        -1    male   27
            2        -1  female   30
            3        -1  female   28

        """

        if not isinstance(series, pd.Series):
            raise TypeError(
                f"Expected object of type 'pd.Series' but got {type(series)}"
            )

        series = series.mask(series != name, -1)
        series = series.mask(series == name, 1)

        return series
