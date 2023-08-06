"""
SphynxMLA predictive analytics functionality.

Supports (binary and multiclass) classification and regression supervised ML tasks. Uses
EvalML AutoML system for hyperparameter optimization and best-performing model search.
The user can define specific AutoML hyperparameters, according to the analysis
prerequisites. Through MlFlow, supports model versioning and analysis metadata storage.
"""
import json
import os
import uuid
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd
from evalml import automl
from evalml.problem_types import detect_problem_type
from sklearn import metrics

from sphynxml.BaseModeler import BaseModeler
from sphynxml.utils._mlflow import (
    mlflow_create_experiment,
    mlflow_log_analysis_metadata,
    retrieve_production_model,
    retrieve_production_model_metadata,
)


class SphynxPredictor(BaseModeler):
    """
    Creates ML models for predictive classification/regression tasks. Also used for
    making predictions on new data and evaluating the predictive performance of an
    active ML model.

    Parameters:
        experiment_name (str): The use case name which this class object corresponds to
        data_origin (Optional[str]): The origin of the train data (currently only
        Elastic)
        task_specific_variables (Optional[dict]): Special variables dict dedicated to
        specific use cases
        tracking_uri (Optional[str]): The uri corresponding to the mlflow tracking
        server
    """

    def __init__(
        self,
        experiment_name: str,
        user: str,
        mlflow_flag: Optional[bool] = True,
        tracking_uri: Optional[str] = "http://192.168.1.14:9431/",
        data_origin: Optional[str] = None,
        task_specific_variables: Optional[Dict[str, str]] = None,
    ) -> None:

        super().__init__()

        self.experiment_name = experiment_name
        self.user = user
        self.data_origin = data_origin
        self.mlflow_flag = mlflow_flag
        self.tracking_uri = tracking_uri
        if task_specific_variables is not None:
            if isinstance(task_specific_variables, dict):
                self.task_specific_variables = task_specific_variables
            else:
                raise TypeError("use case specific variables muct be a dict")

        self.meta["modeler_type"] = "predictor"
        self.meta["data_type"] = "tabular"

    def fit(
        self,
        train_data: Union[pd.DataFrame, np.ndarray],
        train_target: pd.Series,
        train_data_ids: pd.Series,
        automl_hyperparameters,
    ) -> Dict:
        """
        Fit a predictive ML pipeline for a specific use case on the desired train data.
        Currently only supports supervised tasks [classification (binary and multiclass)
        and regression]. The user is able to customize some of the AutoML
        hyperparameters. Once the analysis is completed, the parameters, train
        performance metrics and other artifacts are saved. The resulted pipeline will be
        logged in the mlflow tracking server and will be staged as 'Production', thus
        used for future predictions and model performance evaluation.

        Parameters:
            train_data (pd.DataFrame): The train data without the target variable
            train_target (pd.Series): The train target variable
            train_data_ids (list): The train data ids corresponding to the Elastic
                samples.
            problem_type (Optional[str]): Can be 'binary', 'multiclass' or 'regression'.
                Defaults to None, problem type is automatically inferred from the
                train_target.
            tolerance (Optional[int]): Enables early stopping during the pipeline
                optimization. It corresponds to the number of rounds AutoML will try
                optimizing an already optimized pipeline. Defaults to Disabled.
            time_budget (Optional[int]): How much is the time budget (in seconds) for
                the pipeline optimization. Defaults to 60 seconds.
            allowed_model_families (Optional[list]): The user can decide which of the
                available predictive models will be included in the pipeline
                optimization. Defaults to all.
            ensembling (Optional[bool]): Whether to enable ensembling.
                Defaults to False.
            n_jobs (Optional[int]): How many cores to use for this pipeline.
                optimization. -1 corresponds to all available cores. Defaults to 1.
            verbose (Optional[bool]): Show information during pipeline optimization.
                Defaults to True.

        Returns:
            Training performance metrics of the best performing pipeline

        Raises:
            TypeError: Invalid input type
            ValueError: Invalid input value

        Example:
            # TODO: Add example
            >>>
            >>>
            >>>
            >>>
            >>>
            >>>

        """
        # Perform input checks and throw Exceptions in case of bad input.
        if not isinstance(train_data, pd.DataFrame):
            raise TypeError("Train data type must be pd.DataFrame")
        if isinstance(train_target, pd.Series):
            if train_target.empty:
                raise ValueError("Empty train target")
        else:
            raise TypeError("Train target type must be pd.Series")

        if not isinstance(train_data_ids, pd.Series):
            raise TypeError("train_data_ids must be of type pd.Series")

        problem_type = automl_hyperparameters.get("problem_type", None)
        if problem_type is not None:
            if not (problem_type in ["binary", "multiclass", "regression"]):
                raise ValueError("Invalid problem type.")

        tolerance = automl_hyperparameters.get("tolerance", None)
        if tolerance is not None:
            if (not isinstance(tolerance, int)) | (tolerance <= 0):
                raise TypeError("Tolerance must be a positive integer.")

        max_time = automl_hyperparameters.get("time_budget", 60)
        if (not isinstance(max_time, int)) | (max_time <= 0):
            raise TypeError("Max time must be a positive integer.")

        included_model_families = automl_hyperparameters.get(
            "included_model_families", None
        )
        if included_model_families is not None:
            if not isinstance(included_model_families, list):
                raise TypeError("included_model_families must be a list")

        ensembling = automl_hyperparameters.get("ensembling", False)
        if not isinstance(ensembling, bool):
            raise TypeError("ensembling must be a boolean")

        n_jobs = automl_hyperparameters.get("n_jobs", 1)
        if not isinstance(n_jobs, int) | ((n_jobs <= 0) & (n_jobs != -1)):
            raise ValueError("n_jobs can be a positive integer or -1")

        verbose = automl_hyperparameters.get("verbose", True)
        if not isinstance(verbose, bool):
            raise TypeError("verbose must be a boolean")

        run_name = "predictive_" + self.experiment_name + "_" + str(uuid.uuid4())

        if self.mlflow_flag:
            mlflow = mlflow_create_experiment(
                self.experiment_name, run_name, self.tracking_uri
            )

        # evalml problem type inference from the target variable
        if problem_type is None:
            problem_type = detect_problem_type(train_target)

        objective = None
        if str(problem_type) == "binary":
            objective = "f1"
        elif str(problem_type) == "multiclass":
            objective = "f1 micro"
        elif str(problem_type) == "regression":
            objective = "r2"
        else:
            raise ValueError("Invalid problem type")

        # evalml object creation for model tuning
        eval_automl = automl.AutoMLSearch(
            X_train=train_data,
            y_train=train_target,
            problem_type=problem_type,
            tolerance=tolerance,
            max_time=max_time,
            allowed_model_families=included_model_families,
            ensembling=ensembling,
            n_jobs=n_jobs,
            verbose=verbose,
            objective=objective,
        )

        # evalml best model search and selection
        eval_automl.search()
        best_pipeline = eval_automl.best_pipeline
        print(best_pipeline.name)
        # mlflow logged parameters
        params_dict = {
            "objective": objective,
            "tolerance": tolerance,
            "max_time": max_time,
            "ensembling": ensembling,
            "n_jobs": n_jobs,
        }

        # mlflow stored performance results
        metrics_dict = {
            "train_performance": eval_automl.full_rankings.iloc[0]["mean_cv_score"],
            "internal_validation_performance": eval_automl.full_rankings.iloc[0][
                "validation_score"
            ],
        }

        # mlflow stored tags
        tags_dict = {
            "data-origin": self.data_origin,
            "use-case": self.experiment_name,
        }

        artifacts_path = f"/home/Workflows/{self.user}/{run_name}_artifacts"
        artifacts_dict = {
            "problem_type": str(problem_type),
            "target_variable": train_target.name,
            "best_pipeline_name": best_pipeline.name,
            "train_performance": metrics_dict["train_performance"],
            "included_data_features": train_data.columns.values.tolist(),
            "train_ids": train_data_ids.values.tolist(),
            "run_name": run_name,
            # "run_id": mlflow.info.run_id,
            "model_name": self.experiment_name + "_predictive-model",
            # TODO: When revisiting versioning this must be fixed
            "model_version": 1,
            "artifact_path": artifacts_path,
        }

        # TODO: Clean this somehow. Needs testing with GUI
        eval_automl.rankings.to_csv(f"/home/mlearning/{self.experiment_name}.csv")
        rankings_csv = pd.read_csv(f"/home/mlearning/{self.experiment_name}.csv")
        try:
            os.remove(f"/home/mlearning/{self.experiment_name}.csv")
        except Exception as e:
            print(f"{e.__class__} Exception occured")
            print(f"File: '/home/mlearning/{self.experiment_name}.csv' not found")
        # shutil.rmtree(f"/home/mlearning/{self.experiment_name}.csv")
        artifacts_dict["automl_rankings"] = json.loads(rankings_csv.to_json())

        # change this to dynamic user folder
        if not os.path.exists(artifacts_path):
            os.makedirs(artifacts_path)
        with open(artifacts_path + "/train_artifacts.json", "w") as handle:
            json.dump(artifacts_dict, handle)

        # shutil.rmtree(run_name + "_artifacts")

        if self.mlflow_flag:
            mlflow_log_analysis_metadata(
                mlflow,
                self.tracking_uri,
                self.experiment_name,
                best_pipeline,
                artifacts_path,
                params_dict,
                metrics_dict,
                tags_dict,
            )
        self._best_pipeline = best_pipeline

        return artifacts_dict

    def predict(self, test_data):
        """
        Retrieve the model staged as 'Production' for the use case defined during the
        class object creation and predict the labels of the test data

        Parameters:
            test_data (pd.DataFrame): The test data we want to predict their labels on

        Returns:
            test_predictions (pd.Series): The predicted labels of the test data

        Raises:
            TypeError: Invalid test_data type

        Example:
            # TODO: fill example

        """

        # input integrity checks
        if not isinstance(test_data, pd.DataFrame):
            raise TypeError("test_data must be of type pd.DataFrame")

        model_metadata = retrieve_production_model_metadata(self.experiment_name)

        model = retrieve_production_model(self.experiment_name)

        results = {"predictions": None, "predictions_proba": None}
        # test_data_variables = set(test_data.columns.values.tolist())
        # common_variables = list(
        #     test_data_variables.intersection(
        #         set(model_metadata["included_data_features"])
        #     )
        # )
        results["predictions"] = model.predict(
            test_data[model_metadata["included_data_features"]]
        )
        if model_metadata["problem_type"] != "regression":
            predictions_proba = model.predict_proba(
                test_data[model_metadata["included_data_features"]]
            )
            results["predictions_proba"] = predictions_proba
        self._prediction_results = results

        return results

    def score(self, test_target=None, test_predictions=None):
        """
        Score the predictive performance of the best model by evaluating it based on
        various metrics.

        Parameters:
            test_target (pd.Series): The true labels of the test data
            test_predictions (pd.Series): The predicted labels of the test data

        Returns:
            performance_results (dict): A dictionary containing various predictive
            performance metrics.

        Raises:
            ValueError: Invalid input type

        Example:
            # TODO: fill the example
        """
        # input integrity checks
        if (test_target is None) | (test_predictions is None):
            raise ValueError("test_target and test_predictions must be pd.Series")

        model_metadata = retrieve_production_model_metadata(self.experiment_name)

        # test performance estimation
        if model_metadata["problem_type"] != "regression":
            performance_results = {
                "f1_micro": metrics.f1_score(
                    test_target.values.tolist(),
                    test_predictions.values.tolist(),
                    average="micro",
                ),
                "balanced_acc": metrics.balanced_accuracy_score(
                    test_target.values.tolist(), test_predictions.values.tolist()
                ),
                "precision_micro": metrics.precision_score(
                    test_target.values.tolist(),
                    test_predictions.values.tolist(),
                    average="micro",
                ),
                "recall_micro": metrics.recall_score(
                    test_target.values.tolist(),
                    test_predictions.values.tolist(),
                    average="micro",
                ),
            }
        else:
            performance_results = {
                "r2": metrics.r2_score(
                    test_target.values.tolist(), test_predictions.values.tolist()
                ),
                "neg_mean_squared_error": metrics.mean_squared_error(
                    test_target.values.tolist(), test_predictions.values.tolist()
                ),
                "neg_mean_absolute_percentage_error": (
                    metrics.mean_absolute_percentage_error(
                        test_target.values.tolist(), test_predictions.values.tolist()
                    )
                ),
                "explained_variance": metrics.explained_variance_score(
                    test_target.values.tolist(), test_predictions.values.tolist()
                ),
            }
        self._performance_results = performance_results
        return performance_results
