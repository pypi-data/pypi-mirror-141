"""
Manages the execution of statistical tests and the tracking of the the results.

"""

import json
import os
import uuid
from typing import Optional

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient

from sphynxml.BaseModeler import BaseModeler
from sphynxml.Statistics.Statistics import InfoStats, SummaryStatistics


class SphynxStatistics(BaseModeler):
    """
    Initializes the tracking of the results with MLFLow.

    Parameters:
        use_case (str): The statistical test to run
        data_origin (Optional[str]):The source of data (default: "elk")
        tracking_uri (Optional[str]): The MLFlow tracking uri (default: "http://192.168.1.14:9431/")

    """

    def __init__(
        self,
        use_case: str,
        data_origin: Optional[str] = "elk",
        tracking_uri: Optional[str] = "http://192.168.1.14:9431/",
    ) -> None:

        super().__init__()

        if use_case is None:
            raise ValueError("Use case must be non-empty str")
        self.use_case = use_case

        if data_origin in ["elk"]:
            self.data_origin = data_origin
        else:
            raise ValueError("Only elastic data origin currently supported")

        self.meta["modeler_type"] = "statistics"
        self.meta["data_type"] = "tabular"

        self.tracking_uri = tracking_uri
        self.client = MlflowClient(tracking_uri=self.tracking_uri)
        mlflow.set_tracking_uri(self.tracking_uri)

    def fit_statistics(self, stat_type: str, data: pd.DataFrame()) -> pd.DataFrame:
        """Based on the stat_type parameter, calls the proper function to apply
        the respective statistics.

        Parameters:
            stat_type (str): the type of the statistic to apply
            data (pd.DataFrame): the data to be analysed

        Returns:
            A Dataframe with the statistical results

        Example:

        """

        # set the experiment to the corresponding use_case. If it doesnt exist, create it
        mlflow.set_experiment("statistics_" + self.use_case)

        # create unique run_name for this pipeline creation
        run_name = "statistics_" + self.use_case + "_" + str(uuid.uuid4())
        mlflow.start_run(run_name=run_name)
        run = mlflow.active_run()

        print("Active run_id: {}".format(run.info.run_id))

        mlflow.log_param("statistics type", stat_type)

        if stat_type == "info":
            stats_model = InfoStats()
            res = stats_model.get_info_stats(data)
            res_dict = res.to_dict()

            artifacts_dict = {
                "nan_number": res_dict["Number of NaN"],
                "missing_values": res_dict["NaN percentage"],
                "obj_type": res_dict["Type"],
            }

        elif stat_type == "summary":
            stats_model = SummaryStatistics()
            res = stats_model.get_summary_stats(data)
            res_dict = res.T.to_dict()
            artifacts_dict = {key: res_dict[key] for key in res_dict.keys()}

        elif stat_type == "inferential":
            # TODO: ADD inferential call
            pass

        mlflow.log_metrics = artifacts_dict

        if not os.path.exists("statistics_" + self.use_case + "_artifacts"):
            os.makedirs("statistics_" + self.use_case + "_artifacts")
        with open(
            "statistics_" + self.use_case + "_artifacts/statistics_results.json", "w"
        ) as handle:
            json.dump(artifacts_dict, handle)
        mlflow.log_artifact("statistics_" + self.use_case + "_artifacts")
        mlflow.sklearn.log_model(stats_model, "statistics-model")
        mlflow.end_run()

        return artifacts_dict
