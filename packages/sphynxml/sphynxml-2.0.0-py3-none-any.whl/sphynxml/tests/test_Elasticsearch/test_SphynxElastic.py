import json
import pytest

from datetime import datetime
from pathlib import Path
from sphynxml.Elasticsearch.SphynxElastic import SphynxElastic


def test_elastic_missing_credentials():
    """
    | GIVEN   A SphynxElastic object
    | WHEN    Try to connect to elastic client with no credentials
    | THEN    A RuntimeError exception is raised
    """
    elastic = SphynxElastic()
    with pytest.raises(RuntimeError) as excinfo:
        elastic.connect()

    assert str(excinfo.value) == "Missing credentials"


def test_elastic_connection():
    """
    | GIVEN   A path to a json file with elastic credentials
    | WHEN    Try to connect to elastic client with the credentials
    | THEN    A successful connection should be established
    """
    credentials_path = Path("sphynxml/Elasticsearch/sphynx_elastic_credentials.json")
    with open(credentials_path) as f:
        credentials_j = json.load(f)

    elastic = SphynxElastic()
    es = elastic.connect(credentials_j)

    assert es.ping()


def test_elastic_empty_query():
    """
    | GIVEN   A path to a json file with elastic credentials
    | A start date
    | A finish date, same with the start date
    | WHEN    Querying elastic search using timeframe [start, finish]
    | THEN    No entries should be returned
    """
    credentials_path = Path("sphynxml/Elasticsearch/sphynx_elastic_credentials.json")
    with open(credentials_path) as f:
        credentials_j = json.load(f)

    elastic = SphynxElastic()
    elastic.connect(credentials_j)

    start = datetime(2021, 9, 1)
    end = datetime(2021, 9, 1)

    elastic_data = elastic.query_elastic(
        "UEBA: User Credentials Compromisation", start, end
    )

    assert elastic_data.shape == (0, 0)


def test_elastic_query_size_limit():
    """
    | GIVEN   A path to a json file with the elastic credentials
    | A number of samples to fetch (size)
    | WHEN    Querying elastic with size = size
    | THEN    The returned number of samples should be equal to size
    """
    credentials_path = Path("sphynxml/Elasticsearch/sphynx_elastic_credentials.json")
    with open(credentials_path) as f:
        credentials_j = json.load(f)

    elastic = SphynxElastic()
    elastic.connect(credentials_j)

    elastic_data = elastic.query_elastic(
        use_case="UEBA: User Credentials Compromisation",
        time_from=datetime(2021, 9, 1),
        size=10,
    )

    assert elastic_data.shape == (10, 49)
