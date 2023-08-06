"""
Connectivity with elasticsearch search engine.

Supports communication with the elasticsearch search engine. Querying to
elasticsearch is based on pre-defined queries, specially engineered to
fit the needs of spesific use-cases. In most cases, the user can
parameterize the query using the match, size, timeframe and fields
parameters.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
from elasticsearch import Elasticsearch, RequestsHttpConnection

from sphynxml.BaseModeler import BaseModeler
from sphynxml.Elasticsearch.tests.SphynxElastic_tests import (
    _check_connection,
    _check_true_value,
)
from sphynxml.utils._elasticsearch import ms_to_datetime


class SphynxElastic(BaseModeler):
    """
    Connects to an Elasticsearch client and executes queries. The data can be
    filtered based on a time interval, the size and the fields.
    """

    def __init__(self, logger_name: Optional[str] = None) -> None:
        return

    def __str__(self) -> str:
        return str(self.es.info())

    def connect(
        self,
        credentials: Dict = None,
    ) -> Elasticsearch:
        """
        Creates a connection to an elasticsearch client.

        Args:
            credentials (Dict): A dictionary with the credentials
        Returns:
            An elasticsearch client.
        Raises:
            RuntimeError: Wrong credential values
            RuntimeError: Unable to connect to a client
        """

        if credentials is None:
            raise RuntimeError("Missing credentials")

        ip = credentials.get("ip", None)
        port = credentials.get("port", None)
        name = credentials.get("name", None)
        password = credentials.get("password", None)

        if ip is None:
            raise RuntimeError("IP is missing.")
        if port is None:
            raise RuntimeError("Port is missing.")
        if name is None:
            raise RuntimeError("User-name is missing.")
        if password is None:
            raise RuntimeError("Password is missing.")

        self.es = Elasticsearch(
            hosts=ip,
            port=port,
            http_auth=(name, password),
            connection_class=RequestsHttpConnection,
            scheme="https",
            use_ssl=True,
            verify_certs=False,
        )

        # Check connection status
        if _check_connection(self.es):
            print(self.es.info())
            return self.es
        else:
            raise ConnectionError("Connection failed. Check credentials.")

    def _all_indices(self) -> List[str]:
        """
        Returns all the indices of the elastic client.

        Returns:
            A list of all the elastic indices
        """

        indices = self.es.indices.get_alias("*")
        return indices

    def _filebeat_indices(self) -> List[str]:
        """
        Searches and returns all the filebeat indices.

        Returns:
            The names of all the filebeat indices
        """

        indices = []
        all_indexes = self._all_indices()
        for key in all_indexes:
            if "filebeat" in key:
                indices.append(key)

        return indices

    def _query_filebeat(
        self, query: Dict, index: str, size: Optional[int] = 4096
    ) -> pd.DataFrame:
        """
        Executes a query to a specific filebeat index and transforms the result
        to a DataFrame.

        Parameters:
            query (dict): the query for the elastic properly formated as a dictionary
            index (Optional[str]): The elastic index (default: None)
            size (Optional[int]): The maximum number of values to query (default: 4096)

        Returns:
            A DataFrame with the results of the query to a specific filebeat
        """

        q_dic = self.es.search(index=index, body=query, size=size)
        _check_true_value(q_dic, size)
        # Flatten the dictionary
        q_df = pd.json_normalize(q_dic["hits"]["hits"], sep=":")

        return q_df

    def _exec_query(
        self, query: Dict, index: Optional[str] = "_all", size: Optional[int] = 4096
    ) -> pd.DataFrame:
        """
        Executes queries to all or specific filebeat indices.

        Args:
            query (dict): The query for the elastic properly formated as a dictionary
            index (Optional[str]): The elastic index (default: "_all")
            size (Optional[int]): The maximum number of values to query (default: 4096)

        Returns:
            The query results from the specified filebeats formated in a pandas frame
        """

        res_df = pd.DataFrame()
        if index == "_all":
            filebeat_index = self._filebeat_indices()

            for f_index in filebeat_index:
                q_df = self._query_filebeat(query, f_index, size)
                res_df = res_df.append(q_df)

                if res_df.shape[0] >= size:
                    res_df = res_df.iloc[:size, :]
                    break
        else:
            res_df = self._query_filebeat(query, index, size)

        return res_df

    def _fetch_uc_query(
        self,
        use_case: str,
        start: datetime,
        end: datetime,
        fields: Optional[List] = ["*"],
        ids: Optional[List] = None,
    ):
        """
        Maps a specified use-case to the respective query.

        Parameters:
            use_case (str): The use case name
            start (datetime): The start of the query timeframe
            end (datetime): The end of the query timeframe
            fields (Optional[List]): A list of the fields to fetch

        Returns:
            The proper query for the specific use-case in a dictionary format
        """

        query = None
        if use_case == "UEBA: User Credentials Compromisation":
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"event.action": "ssh_login"}},
                            {"range": {"@timestamp": {"gte": start, "lt": end}}},
                        ]
                    }
                },
                "sort": [{"@timestamp": {"order": "desc"}}],
                "_source": fields,
            }

            if ids is not None:
                id_query_field = {"terms": {"_id": ids}}
                query["query"]["bool"]["must"].append(id_query_field)

        else:
            raise ValueError(
                "Use-case parameter value does not match any available use-cases."
            )
        return query

    def query_elastic(
        self,
        use_case: str,
        time_from: Union[int, datetime],
        time_until: Optional[Union[int, datetime]] = datetime.now(),
        size: Optional[int] = 10000,
        fields: Optional[List] = ["*"],
        index: Optional[str] = "_all",
        ids: Optional[List] = None,
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Based on the use-case, executes the proper query and returns the data.

        Parameters:
            use_case (str): The use-case name
            timeframe (int, datetime, List):
            size (Optional[int]):
            index (Optional[str]):
            fields (Optional[List]):

        Returns:
            The query resutls
        """

        if isinstance(time_from, int):
            time_from = ms_to_datetime(time_from)

        if isinstance(time_until, int):
            time_until = ms_to_datetime(time_until)

        query = self._fetch_uc_query(use_case, time_from, time_until, fields, ids)
        query_data = self._exec_query(query, index, size)

        if query_data.empty:
            print("Query returned no entries.")
            return pd.DataFrame()

        # Remove '_source:' str from the start of every columns name
        query_data.columns = list(
            map(lambda x: x.replace("_source:", ""), query_data.columns)
        )
        # Drop "sort" column
        if "sort" in query_data.columns:
            query_data = query_data.drop(columns=["sort"])

        return query_data
