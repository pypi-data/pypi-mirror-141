"""
Provides methods to perform a wide number of statistical tests.

The module consists of three sub-classes, namely the InfoStats, the
SummaryStatistics and the InferentialStatistics. The InfoStats gives general
information about the nature of the data. It calculates the number and
percentage of missing values, the types of the features, etc. The
SummaryStatistics class, calculates the summary statistics of the data. It
returns the mean, median, min, max and percentiles of different thresholds.
Lastly, the InferentialStatistics has methods for estimating parameters and
hypothesis testing.

"""

from typing import Optional, Tuple, Union

import pandas as pd
from scipy.stats import f_oneway, pearsonr, spearmanr
from statsmodels.stats.outliers_influence import variance_inflation_factor


class InfoStats:
    """Calculates basic information about a dataset."""

    def __init__(self) -> None:
        return

    def get_nan_percentage(
        self, data: Union[pd.Series, pd.DataFrame]
    ) -> Union[float, pd.Series]:
        """Calculates the percentage of NaN values.

        Parameters:
            data (Union[pd.Series, pd.DataFrame]): The dataset

        Returns:
            A single value or a list of values that indicate the percentage
            of NaN values in a pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import InfoStats
            >>> data = {'Name': ['Andreas', 'Iordanis', np.nan,'Jane', 'Mary'],
            ... 'Age': ['23', np.nan, '20', np.nan, np.nan]}
            >>> df = pd.DataFrame(data)
            >>> infs = InfoStats()
            >>> res = infs.get_nan_percentage(df)

            >>> res
            Name    20.0
            Age     60.0

        """
        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        num_of_samples = data.shape[0]
        num_of_nan = data.isnull().sum()

        per_of_nan = 100 * num_of_nan / num_of_samples
        per_of_nan = per_of_nan.fillna(0)

        return per_of_nan

    def get_info_stats(self, data: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """Calculates the number and percentage of NaN values and the type of
        the features.

        Parameters:
            data (Union[pd.Series, pd.DataFrame]): The dataset

        Returns:
            A dataFrame with the number and percentage of NaN values and the
            type of the features

        Examples:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import InfoStats
            >>> data = {'Name': ['Andreas', 'Iordanis', np.nan,'Jane', 'Mary'],
            ... 'Age': [23, np.nan, 20, np.nan, np.nan]}
            >>> df = pd.DataFrame(data)
            >>> infs = InfoStats()
            >>> res = infs.get_info_stats(df)

            >>> res
                  Num of NaN  Missing values %    Type
            Name           1              20.0  object
            Age            3              60.0   int64

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        # TODO: handle num of features and samples (return)
        # num_of_features = data.shape[1]
        # num_of_samples = data.shape[0]

        num_of_nan = data.isnull().sum()
        missing_percentage = self.get_nan_percentage(data)
        feature_types = data.dtypes

        res = pd.concat([num_of_nan, missing_percentage, feature_types], axis=1)
        res.columns = ["Num of NaN", "Missing values %", "Type"]

        return res


class SummaryStatistics:
    """Calculates the summary statistics of a dataset."""

    def __init__(self, logger_name: Optional[str] = None) -> None:
        return

    def get_mode(self, data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        """Calculates the mode. The parameter can either be a pandas Series
        or pandas DataFrame. In case of pandas Series object, then the method
        returns a scalar value which is the mode value of all the observations
        in the dataframe. In case of pandas DataFrame object, then the method
        returns a pandas series object which contains the mode of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the mode of the
            pd.Series or pd.DataFrame dataset respectively

        Examples:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_mode(df)

            >>> res
                 Name  Age
            0  George   26

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        d_m = data.mode()

        return d_m

    def get_mean(self, data: Union[pd.DataFrame, pd.Series], axis: Optional[int] = 0):
        """Calculates the mean. The parameter can either be a pandas Series
        or pandas DataFrame. In case of pandas Series object, then the method
        returns a scalar value which is the mean value of all the observations
        in the dataframe. In case of pandas DataFrame object, then the method
        returns a pandas series object which contains the mean of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the mean of the
            pd.Series or pd.DataFrame dataset respectively

        Examples:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_mean(df)

            >>> res
            Age    25.75
            dtype: float64

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.select_dtypes(include="number").mean()

    def get_median(self, data: Union[pd.DataFrame, pd.Series], axis: Optional[int] = 0):
        """Calculates the median. The parameter can either be a pandas Series
        or pandas DataFrame. In case of pandas Series object, then the method
        returns a scalar value which is the median value of all the observations
        in the dataframe. In case of pandas DataFrame object, then the method
        returns a pandas series object which contains the median of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the median of the
            pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_median(df)

            >>> res
            Age    26.0
            dtype: float64

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.select_dtypes(include="number").median()

    def get_max(self, data: Union[pd.DataFrame, pd.Series], axis: Optional[int] = 0):
        """Calculates the max value. The parameter can either be a pandas Series
        or pandas DataFrame. In case of pandas Series object, then the method
        returns a scalar value which is the max value of all the observations
        in the dataframe. In case of pandas DataFrame object, then the method
        returns a pandas series object which contains the max of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the max of the
            pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_max(df)

            >>> res
            Name    Penny
            Age        31
            dtype: object

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.max(axis=axis)

    def get_min(self, data: Union[pd.DataFrame, pd.Series], axis: Optional[int] = 0):
        """Calculates the min. The parameter can either be a pandas Series
        or pandas DataFrame. In case of pandas Series object, then the method
        returns a scalar value which is the min value of all the observations
        in the dataframe. In case of pandas DataFrame object, then the method
        returns a pandas series object which contains the min of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the min of the
            pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_min(df)

            >>> res
            Name    George
            Age         20

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.min(axis=axis)

    def get_std(self, data: Union[pd.Series, pd.DataFrame], axis: Optional[int] = 0):
        """Calculates the standard deviation(std). The parameter can either
        be a pandas Series or pandas DataFrame. In case of pandas Series object,
        then the method returns a scalar value which is the std value of all
        the observations in the dataframe. In case of pandas DataFrame object,
        then the method returns a pandas series object which contains the std
        of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the std of the
            pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_std(df)

            >>> res
            Age    4.5
            dtype: float64

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.select_dtypes(include="number").std(axis=axis)

    def get_quantile(
        self,
        data: Union[pd.Series, pd.DataFrame],
        q: Optional[float] = 0.5,
        axis: Optional[int] = 0,
    ):
        """Calculates the value of the given quantile. The parameter can either
        be a pandas Series or pandas DataFrame. In case of pandas Series object,
        then the method returns a scalar value which is the quantile value of all
        the observations in the dataframe. In case of pandas DataFrame object,
        then the method returns a pandas series object which contains the quantile
        of the values.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset
            axis (Optional[int]): Specifies the axis

        Returns:
            A single value or a list of values that indicate the q-quantile of
            the pd.Series or pd.DataFrame dataset respectively

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_quantile(df, .75)

            >>> res
            Age    27.25
            Name: 0.75, dtype: float64

        """

        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        return data.quantile(q)

    def get_summary_stats(self, data: Union[pd.Series, pd.DataFrame]):
        """Returns descriptive statistics. For numeric data, the result's index will
        include count, mean, std, min, max as well as lower, 50 and upper percentiles.
        By default the lower percentile is 25 and the upper percentile is 75. The 50
        percentile is the same as the median. For object data (e.g. strings or timestamps),
        the result's index will include count, unique, top, and freq. The top is the most
        common value. The freq is the most common value's frequency. Timestamps also include
        the first and last items.

        Parameters:
            data (Union[pd.DataFrame, pd.Series]): The dataset

        Returns:
            Summary statistics of the Series or Dataframe provided.

        Example:
            >>> import pandas as pd
            >>> import numpy as np
            >>> from sphynxml.Statistics.Statistics import SummaryStatistics
            >>> data = {'Name': ['George', 'Michalis', 'George', 'Penny'],
            ... 'Age': [26, 26, 20, 31]}
            >>> df = pd.DataFrame(data)
            >>> ss = SummaryStatistics()
            >>> res = ss.get_summary_stats(df)

            >>> res
                      Name    Age
            count        4   4.00
            unique       3    NaN
            top     George    NaN
            freq         2    NaN
            mean       NaN  25.75
            std        NaN   4.50
            min        NaN  20.00
            25%        NaN  24.50
            50%        NaN  26.00
            75%        NaN  27.25
            max        NaN  31.00

        """
        if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        sum_stats = data.describe(include="all")

        return sum_stats


class InferentialStatistics:
    """Calculates the inferential statistics between two datasets."""

    def __init__(self) -> None:
        return

    def variance_inflation_factor(self, data: pd.DataFrame):
        """
        Quantifies the severity of multicollinearity in an ordinary least squares
        regression analysis.

        Parameters:
            data (pd.DataFrame, pd.Series): The DataFrame

        Returns:
            A dataframe with the names of the numeric columns and the respective
            variance inflation factor value

        """

        # TODO: add parameter exog_idx, check documentation

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(data)}"
            )

        # TODO: drop nan, inf, etc is mandatory
        # TODO: Numeric only (add check)
        # TODO: Add check for length, if 1 return
        vif_data = [
            variance_inflation_factor(data.values, i) for i in range(len(data.columns))
        ]
        vif_data = pd.Series(vif_data, index=data.columns)

        return vif_data

    # TODO: Check x1,x2 accepted types
    def pearson_corr(self, x1, x2):
        """
        Measure the linear relationship between two datasets. The calculation
        of the p-value relies on the assumption that each dataset is normally distributed.
        The return coefficient varies between -1 and +1 with 0 implying no correlation.
        Correlations of -1 or +1 imply an exact linear relationship.

        Parameters:
            x1: Input array
            x2: Input array

        Returns:
            pc_coef: Pearson's correlation coefficient.
            pc_pvalue: Two-tailed p-value.

        """
        # TODO: re-check .. numpy is also ok
        if not isinstance(x1, pd.Series):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(x1)}"
            )

        if not isinstance(x2, pd.Series):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(x2)}"
            )

        pc_coef, pc_pvalue = pearsonr(x1, x2)

        return pc_coef, pc_pvalue

    def spearman_corr(
        self,
        x1: Union[pd.Series, pd.DataFrame],
        x2: Optional[Union[pd.Series, pd.DataFrame]] = None,
    ) -> Tuple[float, float]:
        """
        The Spearman rank-order correlation coefficient is a nonparametric measure
        of the monotonicity of the relationship between two datasets.

        Parameters:
            x1: Input array
            x2: Input array

        Returns:
            sc_coef: Spearman correlation matrix or correlation coefficient
            sc_pvalue: Two-tailed p-value.

        """
        if not isinstance(x1, pd.Series) and not isinstance(x1, pd.DataFrame):
            raise TypeError(
                "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                f" {type(x1)}"
            )

        if x2 is not None:
            if not isinstance(x2, pd.Series) and not isinstance(x2, pd.DataFrame):
                raise TypeError(
                    "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
                    f" {type(x2)}"
                )

        sc_coef, sc_pvalue = spearmanr(x1, x2)
        return sc_coef, sc_pvalue

    def one_way_anova(
        self, *data: Union[pd.Series, pd.DataFrame]
    ) -> Tuple[float, float]:
        """
        Performs one way anova on the data to determine whether there are any
        statistically significant differences between the means.

        Parameters:
            *data (Union[pd.Series, pd.DataFrame]): The data

        Returns:
            fvalue: The computed F statistic of the test
            pvalue: The associated p-value from the F distribution
        """

        for x in data:
            if not isinstance(x, pd.Series) and not isinstance(x, pd.DataFrame):
                raise TypeError(
                    "Expected objects of type 'pd.DataFrame' or 'pd.Series' but got"
                    f" {type(x)}"
                )

        if len(data) == 1:
            raise RuntimeError("At least two inputs are required; got 1.")

        fvalue, pvalue = f_oneway(*data)

        return fvalue, pvalue
