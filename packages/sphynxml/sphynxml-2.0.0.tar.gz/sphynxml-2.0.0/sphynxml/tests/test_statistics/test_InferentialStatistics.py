import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.oneway import anova_oneway

from sphynxml.Statistics.Statistics import InferentialStatistics


def test_variance_inflation_factor_type_exception():
    """
    | GIVEN   A non pd.DataFrame type object
    | WHEN    Calling the variance_inflation_factor on that object
    | THEN    A TypeError exception is raised
    """

    infs = InferentialStatistics()
    data_list = {"Year": [2020, 2020, 1990, 2020, 2021]}

    with pytest.raises(TypeError) as excinfo:
        infs.variance_inflation_factor(data_list)

    assert (
        str(excinfo.value)
        == "Expected object of type 'pd.DataFrame' or 'pd.Series' but got"
        f" {type(data_list)}"
    )


def test_variance_inflation_factor_two():
    """
    | GIVEN   A pd.DataFrame with two integer type columns
    | WHEN    Calling the variance_inflation_factor on that object
    | THEN    A number for each column is returned, representing the variance inflation
    | factor for each column
    """

    data = {
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    infs = InferentialStatistics()

    res = infs.variance_inflation_factor(data)

    assert res.shape == (2,)
    assert res["Year"] == res["Age"]
    assert res["Age"].round(2) == 10.23


def test_variance_inflation_factor_three():
    """
    | GIVEN   A pd.DataFrame with more that two integer type columns
    | WHEN    Calling the variance_inflation_factor on that object
    | THEN    A number for each column is returned, representing the variance inflation
    | factor for each column
    """

    data = {
        "Year": [2020, 2020, 1990, 2020, 2021],
        "Month": [2, 5, 12, 11, 1],
        "Age": [19, 10, 30, 19, 20],
    }
    data = pd.DataFrame(data)
    infs = InferentialStatistics()

    res = infs.variance_inflation_factor(data)

    assert res.shape == (3,)
    assert res["Year"].round(2) == 10.26
    assert res["Month"].round(2) == 3.74
    assert res["Age"].round(2) == 13.49


def test_pearson_corr_x1_type_exception():
    """
    | GIVEN   A non pd.Series object x1 and a pd.Series object x2
    | WHEN    Calling pearson_corr
    | THEN    A TypeError is raised for object x1
    """

    infs = InferentialStatistics()
    x1 = np.random.randint(50, size=15)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    with pytest.raises(TypeError) as excinfo:
        infs.pearson_corr(x1, x2)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' or 'pd.Series' but got {type(x1)}"
    )


def test_pearson_corr_x2_type_exception():
    """
    | GIVEN   A pd.Series object x1 and a non pd.Series object x2
    | WHEN    Calling pearson_corr
    | THEN    A TypeError is raised for object x2
    """

    infs = InferentialStatistics()
    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)
    x2 = np.random.randint(50, size=15)

    with pytest.raises(TypeError) as excinfo:
        infs.pearson_corr(x1, x2)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' or 'pd.Series' but got {type(x2)}"
    )


def test_pearson_corr():
    """
    | GIVEN   Two pd.Series objects
    | WHEN    Calling pearson_corr
    | THEN    The Pearson correlation coefficient is calculated and returned
    """

    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    infs = InferentialStatistics()

    res = infs.pearson_corr(x1, x2)
    true_coef = x1.corr(x2)

    assert round(res[0], 5) == round(true_coef, 5)


def test_spearman_x1_type_exception():
    """
    | GIVEN   A non pd.Series object x1 and a pd.Series object x2
    | WHEN    Calling spearman_corr
    | THEN    A TypeError is raised for object x1
    """

    infs = InferentialStatistics()
    x1 = np.random.randint(50, size=15)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    with pytest.raises(TypeError) as excinfo:
        infs.spearman_corr(x1, x2)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' or 'pd.Series' but got {type(x1)}"
    )


def test_spearman_x2_type_exception():
    """
    | GIVEN   A pd.Series object x1 and a non pd.Series object x2
    | WHEN    Calling spearman_corr
    | THEN    A TypeError is raised for object x2
    """

    infs = InferentialStatistics()
    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)
    x2 = np.random.randint(50, size=15)

    with pytest.raises(TypeError) as excinfo:
        infs.spearman_corr(x1, x2)

    assert (
        str(excinfo.value)
        == f"Expected object of type 'pd.DataFrame' or 'pd.Series' but got {type(x2)}"
    )


def test_spearman_correlation():
    """
    | GIVEN   Two pd.Series objects
    | WHEN    Calling pearson_corr
    | THEN    The Spearman correlation coefficient is calculated and returned
    """

    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    infs = InferentialStatistics()

    res = infs.spearman_corr(x1, x2)
    true_coef = x1.corr(x2, method="spearman")

    assert round(res[0], 5) == round(true_coef, 5)


def test_one_way_anova_type_exception():
    """
    | GIVEN   A non pd.Series object x1 and a pd.Series object x2
    | WHEN    Calling one_way_anova
    | THEN    A TypeError is raised for object x1
    """

    infs = InferentialStatistics()
    x1 = np.random.randint(50, size=15)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    with pytest.raises(TypeError) as excinfo:
        infs.one_way_anova(x1, x2)

    assert (
        str(excinfo.value)
        == f"Expected objects of type 'pd.DataFrame' or 'pd.Series' but got {type(x1)}"
    )


def test_one_way_anova_unique_runtime_exception():
    """
    | GIVEN   A pd.Series object x1
    | WHEN    Calling one_way_anova
    | THEN    A RuntimeError is raised as at least two parameters must be passed to
    | one_way_anova
    """

    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)

    infs = InferentialStatistics()

    with pytest.raises(RuntimeError) as excinfo:
        infs.one_way_anova(x1)

    assert str(excinfo.value) == "At least two inputs are required; got 1."


def test_one_way_anova():
    """
    | GIVEN   Two pd.Series objects
    | WHEN    Calling the one_way_anova
    | THEN    Calculates the fvalue of the one way anova test
    """

    x1 = np.random.randint(50, size=15)
    x1 = pd.Series(x1)
    x2 = np.random.randint(50, size=15)
    x2 = pd.Series(x2)

    infs = InferentialStatistics()
    res = infs.one_way_anova(x1, x2)
    true_res = anova_oneway([x1, x2])

    assert round(res[0], 5) == round(true_res[0], 5)
    assert round(res[1], 2) == round(true_res[1], 2)
