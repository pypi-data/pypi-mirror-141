"""
Performs the pre-processing steps related to filtering.

The module can detect constant, cardinal and correlated features. By using the
data_filter() method, the user can choose to apply all the available data
filtering methods and drop features with no value.
"""

import logging
from typing import List

import numpy as np
import pandas as pd
import scipy.stats as ss

from sphynxml.BaseModeler import BaseModeler


class SphynxFilterer(BaseModeler):
    """Performs pre-processing filtering."""

    def __init__(self) -> None:
        return

    def constant_features(self, df: pd.DataFrame) -> List:
        """Finds the constant features of a dataset.

        Parameters:
            df (pd.DataFrame): The dataset to be analysed

        Returns:
            A list of names of the constant features

        Example:
            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.Filter import Filter
            >>> data = {'Name': ['Andrew', 'Iordanis', 'Jane', 'Mary'],
            'Country': ['Greece', 'Greece', 'Greece', 'Greece'],
            'Gender': ['male','male','female','female'],
            'Hair': ['short', 'short', 'long', 'long']}
            >>> df = pd.DataFrame(data)
            >>> flt = Filter()
            >>> res = flt.constant_features(df)
            WARNING:root:Dropped constant feature: Country

            >>> res
            ['Country']

        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected object of type 'pd.DataFrame' but got {type(df)}"
            )

        cf = df.columns[df.nunique() <= 1]
        for name in cf:
            logging.warning(f"Dropped constant feature: {name}")

        res = list(cf)
        return res

    # TODO: handle inf values in columns
    def cardinal_features(self, df: pd.DataFrame) -> List:
        """Finds the high cardinal features of a dataset.

        Parameters:
            df (pd.DataFrame): The dataset to be analysed

        Returns:
            A list of names of the cardinal features

        Example:
            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.Filter import Filter
            >>> data = {'Name': ['Andrew', 'Iordanis', 'Jane', 'Mary'],
            ... 'Country': ['Greece', 'Greece', 'Greece', 'Greece'],
            ... 'Gender': ['male','male','female','female'],
            ... 'Hair': ['short', 'short', 'long', 'long']}
            >>> df = pd.DataFrame(data)
            >>> flt = Filter()
            >>> res = flt.cardinal_features(df)
            WARNING:root:Dropped cardinal feature: Name

            >>> res
            ['Name']

        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected object of type 'pd.DataFrame' but got {type(df)}"
            )

        cf = df.columns[(df.nunique() + df.isna().sum()) == df.shape[0]]
        for name in cf:
            logging.warning(f"Dropped cardinal feature: {name}")

        res = list(cf)
        return res

    # TODO: SEND TO STATISTICS
    def _cramers_V_corr(self, x1: pd.Series, x2: pd.Series) -> float:
        """Performs Cramer's V corelation test between two variables

        Parameters:
            x1 (pd.DataFrame): the first variable
            x2 (pd.DataFrame): the second variable

        Returns:
            A number between [0, 1], with 0 indicating no correlation and 1
            indicating high correlation
        """

        if not isinstance(x1, pd.Series):
            raise TypeError(f"Expected object of type 'pd.Series' but got {type(x1)}")
        if not isinstance(x2, pd.Series):
            raise TypeError(f"Expected object of type 'pd.Series' but got {type(x2)}")

        # Cross tabulation: computes a frequency table of the factors
        cb_matrix = pd.crosstab(x1, x2)

        # Chi-square test of independence of variables in a cross tabulation table.
        chi2 = ss.chi2_contingency(cb_matrix)[0]

        # Calcultate the grand total of observations
        n = cb_matrix.sum().sum()

        # Calculate Phi coefficient ^ 2
        phi2 = chi2 / n

        # Extract cross tabulation table dimentions
        r, k = cb_matrix.shape

        # Calculate the Phi coefficient with Bias correction
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))

        # Number of columns with Bias correction
        rcorr = r - ((r - 1) ** 2) / (n - 1)

        # Number of rows with Bias correction
        kcorr = k - ((k - 1) ** 2) / (n - 1)

        # Calculate the correlation value
        cor = np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

        return cor

    def collinear_features(self, df: pd.DataFrame) -> List:
        """Finds the collinear features using the Cramer's V test.

        Parameters:
            df (pd.DataFrame): The dataset to be analysed

        Returns:
            A list of names of the collinear features

        Example:
            >>> import pandas as pd
            >>> from sphynxml.Preprocessors.SphynxFilterer import SphynxFilterer
            >>> data = {
            ...         "Country": ["Greece"] * 100,
            ...         "Gender": ["male"] * 50 + ["female"] * 50,
            ...         "Hair": ["short"] * 50 + ["long"] * 50,
            ...         }
            >>> data = pd.DataFrame(data)
            >>> flt = SphynxFilterer()
            >>> collinear_features = flt.collinear_features(data)
            /home/devmlearning/machine-learning/Sphynx_ML/sphynxml/Preprocessors/SphynxFilterer.py:152: RuntimeWarning: invalid value encountered in double_scalars
            return cor
            WARNING:root:Found collinear features ['Hair', 'Gender']
            WARNING:root:   Dropped ['Gender']
            >>> collinear_features
            ['Gender']

        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected object of type 'pd.DataFrame' but got {type(df)}"
            )

        collinear_feature_names = set()
        search_col = list(df.columns)

        # Iterate through all the features
        for col_name1 in search_col:

            # Mark it as checked by removing it from the list
            if col_name1 in search_col:
                search_col.remove(col_name1)

            # Iterate through all the remaining features
            for col_name2 in search_col:
                # Call Cramers V correlation for the pair of features
                correlation = self._cramers_V_corr(df[col_name1], df[col_name2])

                # Set threshold for correlated features
                if correlation > 0.9:
                    collinear_feature_names.add(col_name2)
                    logging.warning(
                        f"Found collinear features ['{col_name1}',                     "
                        f"   '{col_name2}']"
                    )

                    # Avoid checking it again
                    if col_name2 in search_col:
                        search_col.remove(col_name2)
                        logging.warning(f"\tDropped ['{col_name2}']")

        cf = list(collinear_feature_names)
        return cf

    def data_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies the filtering functions.

        Parameters:
            df (pd.DataFrame): The dataframe that will be filtered

        Returns:
            A filtered dataframe with no constant, cardinal and collinear
            features

        Examples:
            >>> import pandas as pd
            >>> from Filter import Filter
            >>> data = {'Name': ['Andrew', 'Iordanis', 'Jane', 'Mary'],
            ... 'Country': ['Greece', 'Greece', 'Greece', 'Greece'],
            ... 'Gender': ['male','male','female','female'],
            ... 'Hair': ['short', 'short', 'long', 'long']}
            >>> df = pd.DataFrame(data)
            >>> flt = Filter()
            >>> res = flt.data_filter(df)
            WARNING:root:Dropped constant feature: Country
            WARNING:root:Dropped cardinal feature: Name

            >>> res
               Gender   Hair
            0    male  short
            1    male  short
            2  female   long
            3  female   long
        """

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                f"Expected object of type 'pd.DataFrame' but got {type(df)}"
            )

        df = df.drop(self.constant_features(df), axis=1)
        df = df.drop(self.cardinal_features(df), axis=1)
        df = df.drop(self.collinear_features(df), axis=1)

        return df
