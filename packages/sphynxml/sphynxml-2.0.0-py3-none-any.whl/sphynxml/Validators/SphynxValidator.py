"""
SphynxMLA data validity monitoring functionality.

Examines data regarding possible data distribution shifts. Supports methods for continuous,
categorical and mixed tabular data.
"""
import json
import os
import shutil
import uuid
from typing import Dict, List, Optional, Union

import mlflow
import numpy as np
import pandas as pd
from mlflow.tracking import MlflowClient

from SphynxML.BaseModeler import BaseModeler
from SphynxML.Validators.ChiSquaredValidator import ChiSquaredValidator
from SphynxML.Validators.KSValidator import KSValidator
from SphynxML.Validators.MixedTypeTabularValidator import MixedTypeTabularValidator

# from SphynxML.utils._mlflow import retrieve_production_model_metadata
# from SphynxML.utils._mlflow import retrieve_production_model
# from SphynxML.utils._mlflow import archive_production_model


class SphynxValidator(BaseModeler):
    """
    Creates a data validity model to detect data distribution shifts.

    Parameters:
        use_case (str): The use case name which this class object corresponds to
        data_origin (str): The origin of the data (currently only ELK)
        tracking_uri (Optional[str]): The uri corresponding to the mlflow tracking server
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
            raise ValueError("only elk data origin currently supported")

        self.meta["modeler_type"] = "validator"
        self.meta["data_type"] = "tabular"

        # self.model_metadata = retrieve_production_model_metadata(use_case)
        self.tracking_uri = tracking_uri
        self.client = MlflowClient(tracking_uri=self.tracking_uri)
        mlflow.set_tracking_uri(self.tracking_uri)

    def fit(
        self,
        ref_data: Union[pd.DataFrame, np.ndarray],
        test_data: Union[pd.DataFrame, np.ndarray],
        ref_data_ids: List[str],
        test_data_ids: List[str],
        drift_hyperparameters: Optional[Dict],
    ):
        """
        Creates a data validity model and tests the data for data shifts. The available
        methods are Kolmogorov-Smirnoff (KS), Chi-Squared (ChiSquared), and Mixed tabular
        data test (Tabular). The results are logged in the mlflow tracking server.

        Parameters:
            ref_data Union[pd.DataFrame, np.ndarray]: The reference data
            test_data Union[pd.DataFrame, np.ndarray]: The test data
            ref_data_ids List[str]: The reference data ids corresponding to the ELK samples
            test_data_ids List[str]: The test data ids corresponding to the ELK samples
            drift_method str: The data drift detection method to use
            pvalue OPTIONAL[float]: The desired pvalue threshold to be used by the drift detection method
            correction OPTIONAL[str]: Pvalue correction type applied in the drift detection method

        Returns:
            A boolean expressing the existence of data drift in the data

        Raises:
            TypeError: Invalid input type
            ValueError: Invalid input values

        Example:
            # TODO: fill the example

        """
        # TODO: Refine the invalid input error checking
        # Perform input checks and throw Exceptions in case of bad input.
        if (not isinstance(ref_data, pd.DataFrame)) & (
            not isinstance(ref_data, np.ndarray)
        ):
            raise TypeError(
                "reference data type must be of type pd.DataFrame or np.ndarray"
            )
        if (not isinstance(test_data, pd.DataFrame)) & (
            not isinstance(test_data, np.ndarray)
        ):
            raise TypeError("test data type must be of type pd.DataFrame or np.ndarray")

        if isinstance(ref_data_ids, pd.Series):
            if ref_data_ids.shape[0] == 0:
                raise ValueError("ref_data_ids must have at least 1 element")
        else:
            raise TypeError("ref_data_ids must be of type pd.Series")
        if isinstance(test_data_ids, pd.Series):
            if test_data_ids.shape[0] == 0:
                raise ValueError("test_data_ids must have at least 1 element")
        else:
            raise TypeError("test_data_ids must be of type pd.Series")

        drift_method = drift_hyperparameters.get("drift_method", "MixedTabular")
        if not (drift_method in ["KS", "ChiSquared", "MixedTabular"]):
            raise ValueError(
                "Only 'KS', 'ChiSquared' and 'MixedTabular' are currently supported."
            )

        pvalue = drift_hyperparameters.get("pvalue", 0.05)
        if (not (0 < pvalue < 1)) & (not isinstance(pvalue, float)):
            raise ValueError("pvalue takes values in (0,1)")

        correction = drift_hyperparameters.get("correction", "bonferroni")
        if not (correction in ["bonferroni", "fdr"]):
            raise ValueError("Only 'bonferroni', 'fdr' pvalue corrections are allowed")

        # set the experiment to the corresponding use_case. If it doesnt exist, create it
        mlflow.set_experiment("data_val_" + self.use_case)

        # create unique run_name for this pipeline creation
        run_name = "data_val_" + self.use_case + "_" + str(uuid.uuid4())
        mlflow.start_run(run_name=run_name)
        run = mlflow.active_run()

        print("Active run_id: {}".format(run.info.run_id))

        if drift_method == "KS":
            cd = KSValidator(np.array(ref_data), p_val=pvalue, correction=correction)
        elif drift_method == "ChiSquared":
            cd = ChiSquaredValidator(
                np.array(ref_data), p_val=pvalue, correction=correction
            )
        elif drift_method == "MixedTabular":
            cd = MixedTypeTabularValidator(
                np.array(ref_data), p_val=pvalue, correction=correction
            )

        cd_predict = cd.predict(np.array(test_data), drift_type="feature")

        cd_result = cd_predict["data"]
        drift_detected = cd_result["is_drift"]
        drift_detected_flag = int(drift_detected.any())
        mlflow.log_param("pvalue_threshold", pvalue)

        params_dict = {
            "drift_method": drift_method,
            "pvalue": pvalue,
            "pvalue_correction": correction,
        }
        mlflow.log_params(params_dict)

        metrics_dict = {
            "pvalue_thres_corrected": cd_result["threshold"],
            "drift_detected": drift_detected_flag,
        }
        mlflow.log_metrics(metrics_dict)

        # Log data drift detection model
        mlflow.sklearn.log_model(cd, "data-validity-model")

        artifacts_dict = {
            "drift_columns": test_data.columns[np.nonzero(drift_detected)].tolist(),
            "pvalues_corrected": cd_result["p_val"].tolist(),
            "distances": cd_result["distance"].tolist(),
            "train_indeces": ref_data_ids.values.tolist(),
            "test_indeces": test_data_ids.values.tolist(),
            "run_name": run_name,
            "run_id": run.info.run_id,
            "model_name": self.use_case + "_data_validation-model",
        }
        if not os.path.exists(run_name + "_artifacts"):
            os.makedirs(run_name + "_artifacts")
        with open(run_name + "_artifacts/drift_artifacts.json", "w") as handle:
            json.dump(artifacts_dict, handle)
        mlflow.log_artifacts(run_name + "_artifacts")
        shutil.rmtree(run_name + "_artifacts")

        mlflow.end_run()

        return metrics_dict
