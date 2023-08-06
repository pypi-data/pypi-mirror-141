import json
import pandas as pd

from datetime import datetime
from typing import Optional, Union
from pathlib import Path
from sphynxml.BaseModeler import BaseModeler
from sphynxml.Elasticsearch.SphynxElastic import SphynxElastic
from sphynxml.Preprocessors.SphynxEncoder import SphynxEncoder
from sphynxml.Preprocessors.SphynxFilterer import SphynxFilterer
from sphynxml.Preprocessors.SphynxTransformer import SphynxTransformer
from sphynxml.utils._SphynxETL import split_dataset, string_to_datetime


class SphynxETL(BaseModeler):
    def __init__(self):
        self.st = SphynxTransformer()
        self.se = SphynxEncoder()
        self.sf = SphynxFilterer()

    def load_local_data(
        self, path, target_col: Optional[str] = None, split: Optional[bool] = False
    ):
        """
        Loads a CSV file in a pandas frame given a path to the file.

        Parameters:
            path (str): The path to the file
            target_col (Optional[str]): The name of the target feature (default: None)
            split (Optional[bool]): If True, data, ids and target are returned separately (default: True)

        Returns:
            A dataFrame of the data or the data, the ids and the target
            separately, if the split parameter is True

        Example:
            >>> from SphynxETL import SphynxETL
            >>> etl = SphynxETL()
            >>> path = "/home/devmlearning/machine-learning/Sphynx_ML/examples/example_data/Top 250s in IMDB.csv"
            >>> local_data = etl.load_local_data(path)
            >>> local_data
                ranking of movie                   movie name    Year certificate  runtime                      genre  ...            ACTOR 2          ACTOR 3          ACTOR 4    votes metascore GROSS COLLECTION
            0                   1                      Jai Bhim  -2021       TV-MA  164 min               Crime, Drama  ...      Lijo Mol Jose       Manikandan  Rajisha Vijayan   163431       NaN              NaN
            1                   2      The Shawshank Redemption  -1994           R  142 min                      Drama  ...     Morgan Freeman       Bob Gunton   William Sadler  2515762      80.0          $28.34M
            2                   3                 The Godfather  -1972           R  175 min               Crime, Drama  ...          Al Pacino       James Caan     Diane Keaton  1732749     100.0         $134.97M
            3                   4               The Dark Knight  -2008       PG-13  152 min       Action, Crime, Drama  ...       Heath Ledger    Aaron Eckhart    Michael Caine  2466041      84.0         $534.86M
            4                   5        The Godfather: Part II  -1974           R  202 min               Crime, Drama  ...     Robert De Niro    Robert Duvall     Diane Keaton  1202401      90.0          $57.30M
            ..                ...                           ...    ...         ...      ...                        ...  ...                ...              ...              ...      ...       ...              ...
            245               246  Mr. Smith Goes to Washington  -1939      Passed  129 min              Comedy, Drama  ...        Jean Arthur     Claude Rains    Edward Arnold   112642      73.0           $9.60M
            246               247            Gone with the Wind  -1939      Passed  238 min    Drama, History, Romance  ...           Sam Wood      Clark Gable     Vivien Leigh   304725      97.0         $198.68M
            247               248         It Happened One Night  -1934      Passed  105 min            Comedy, Romance  ...  Claudette Colbert  Walter Connolly     Roscoe Karns   100198      87.0           $4.36M
            248               249    The Passion of Joan of Arc  -1928      Passed  114 min  Biography, Drama, History  ...     Eugene Silvain     André Berley   Maurice Schutz    52264       NaN           $0.02M
            249               250                   The General  -1926      Passed   67 min  Action, Adventure, Comedy  ...      Buster Keaton      Marion Mack    Glen Cavender    88022       NaN           $1.03M

            [250 rows x 16 columns]

        """

        data = pd.read_csv(path)

        if split is True:
            data, ids, target = split_dataset(data, target_col)
            return data, ids, target

        return data

    def load_elastic_data(
        self,
        use_case,
        time_from: Optional[Union[int, datetime]] = None,
        time_until: Optional[Union[int, datetime]] = None,
        size: Optional[int] = 10000,
        target_col: Optional[str] = None,
        split: Optional[bool] = False,
    ) -> pd.DataFrame:
        """
        Loads and filters data from elasticsearch based on specified parameters.

        Parameters:
            use_case (str): The requested use case
            time_from (Optional[Union[int, datetime, List]]): Samples before are
            filtered out
            time_until (Optional[Union[int, datetime, List]]): Samples after are
            filtered out
            size (Optional[int]): Limits the number of samples to return
            (default: 10000)
            target_col (Optional[str]): The name of the target feature (default: None)
            split (Optional[bool]): If True, data, ids and target are returned
            separately (default: True)

        Returns:
            A dataFrame of the data or the data, the ids and the target
            separately, if the split parameter is True

        Example:
            >>> from SphynxETL import SphynxETL
            >>> etl = SphynxETL()
            >>> use_case = "UEBA: User Credentials Compromisation"
            >>> from datetime import datetime
            >>> elastic_data = etl.load_elastic_data(use_case)

        """

        credentials_path = Path(
            "sphynxml/Elasticsearch/sphynx_elastic_credentials.json"
        )
        with open(credentials_path) as f:
            credentials_j = json.load(f)

        elastic = SphynxElastic()
        elastic.connect(credentials_j)

        if isinstance(time_from, str):
            time_from = string_to_datetime(time_from)
        if isinstance(time_until, str):
            time_until = string_to_datetime(time_until)

        data = elastic.query_elastic(use_case, time_from, time_until, int(size))

        if split:
            data, ids, target = split_dataset(data, target_col)
            return data, ids, target

        return data

    def _uc_preprocessing(
        self, data: pd.DataFrame, target: pd.Series, use_case_specific_variable: str
    ):

        target = self.se.one_vs_all_encoder(target, use_case_specific_variable)

        data = self.st.expand_timestamp(data, "@timestamp")
        data = self.st.drop_list_columns(data)
        data = self.se.label_encoder(data)

        return data, target

    def apply_preprocessing(
        self,
        data: pd.DataFrame,
        target: Optional[pd.Series] = None,
        use_case: Optional[str] = None,
        use_case_specific_variable: Optional[str] = None,
        id_name: Optional[str] = None,
        filter_flag: Optional[bool] = True,
    ):
        """
        Performs preprocessing filtering and applies specific uce-case preprocessing.

        Parameters:
            data (pd.DataFrame): The dataset
            target (Optional[pd.Series]): The column name of the target (default: None)
            use_case (Optional[str]): The name of the use case (default: None)
            use_case_specific_variable (Optional[str]): The value of the target column
            to predict (default: None)
            id_name (Optional[str]): The column name of the ids (default: None)
            filter_flag (Optional[bool]): Whether to apply filter on the data or not
            (default: True)

        Returns:
            A cleaned preprocessed dataset
        """

        ids = pd.Series(dtype="str")
        if id_name and id_name in data.columns:
            ids = data[id_name]

        if use_case is not None:
            if use_case == "UEBA: User Credentials Compromisation" or use_case == "uc":
                data, target = self._uc_preprocessing(
                    data, target, use_case_specific_variable
                )

        if filter_flag:
            data = self.sf.data_filter(data)

        return data, target, ids
