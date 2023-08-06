from sphynxml.ETL.SphynxETL import SphynxETL


def test_load_local_data():
    """
    | GIVEN   A path to a csv file in the form of a string
    | WHEN    Calling the load_local_data by passing the path as a parameter
    | THEN    The csv file is returned in the form of a pandas DataFrame
    """

    etl = SphynxETL()
    path = "examples/example_data/uc_data_prod.csv"
    data = etl.load_local_data(path)

    assert data.shape == (822, 49)


def test_load_local_data_split():
    """
    | GIVEN   A path to a csv file in the form of a string
    | WHEN    Calling the load_local_data by passing a path, a column name and setting
    | split equal to True
    | THEN    Three objects are returned. The data in the form of a pd.DataFrame, if an
    | "_id" column exists it is returned as a pd.Series and the target column is returned
    | as a pd.Series
    """

    etl = SphynxETL()
    path = "examples/example_data/uc_data_prod.csv"
    data, ids, target = etl.load_local_data(path, target_col="related:user", split=True)

    assert data.shape == (822, 47)
    assert ids.shape == (822,)
    assert target.shape == (822,)


def test_load_elastic_data_uc():
    """
    | GIVEN
    | WHEN    Querying the elastic for the "UEBA: User Credentials Compromisation"
    | use-case
    | THEN    A dataset is returned with all the ssh_logins
    """

    etl = SphynxETL()
    elastic_data = etl.load_elastic_data(
        use_case="UEBA: User Credentials Compromisation",
        time_from="2021-09-01 00:00:00",
        time_until="2021-12-11 00:00:00",
    )

    assert "event:action" in elastic_data.columns
    assert elastic_data["event:action"].nunique() == 1
    assert (elastic_data["event:action"] == "ssh_login").all()


def test_load_elastic_data_uc_split():
    """
    | GIVEN
    | WHEN    Querying the elastic for the "UEBA: User Credentials Compromisation"
    | use-case with split parameter initialized to True
    | THEN    The data, the ids and the target are returned as a DataFrame, a series and a
    | series respectively
    """

    etl = SphynxETL()
    elastic_data, ids, target = etl.load_elastic_data(
        use_case="UEBA: User Credentials Compromisation",
        time_from="2021-09-01 00:00:00",
        time_until="2021-12-11 00:00:00",
        target_col="related:user",
        split=True,
    )

    assert "event:action" in elastic_data.columns
    assert elastic_data["event:action"].nunique() == 1
    assert (elastic_data["event:action"][0] == "ssh_login").all()


def test_apply_preprocessing():
    """
    | GIVEN   An elastic dataset for the "UEBA: User Credentials Compromisation" use-case
    | WHEN    Calling the apply_preprocessing for preprocessing the dataset
    | THEN    A cleaned, filtered dataset is returned with new features
    """

    etl = SphynxETL()
    elastic_data = etl.load_elastic_data(
        use_case="UEBA: User Credentials Compromisation",
        time_from="2021-09-01 00:00:00",
        time_until="2021-12-11 00:00:00",
    )

    data, _, _ = etl.apply_preprocessing(
        elastic_data, elastic_data["related:user"], "uc", "soultatos", filter_flag=True
    )

    assert "month" in data.columns
    assert "hour" in data.columns
    assert elastic_data.shape[1] > data.shape[1]
