import json
import os

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


def mlflow_create_experiment(experiment_name, run_name, tracking_uri):
    """
    Creates an MLflow experiment. If an experiment with this name already exists,
    retrieves it.

    Args:
        experiment_name (str): the use case name
    """
    mlflow.set_tracking_uri(tracking_uri)
    try:
        mlflow.create_experiment(experiment_name)
    except Exception as e:
        print(f"{e.__class__} Exception occured")
        print(f"Experiment: {experiment_name} already exists")
    mlflow.set_experiment(experiment_name)
    mlflow.start_run(run_name=run_name)
    run = mlflow.active_run()
    print("Active run_id: {}".format(run.info.run_id))

    return mlflow


def mlflow_log_analysis_metadata(
    mlflow_inst,
    tracking_uri,
    experiment_name,
    best_pipeline,
    artifacts_path,
    params_dict,
    metrics_dict,
    tags_dict,
):
    print(mlflow_inst)
    print(mlflow_inst.active_run())
    mlflow_inst.log_params(params_dict)
    mlflow_inst.log_metrics(metrics_dict)
    mlflow_inst.set_tags(tags_dict)
    client = MlflowClient(tracking_uri=tracking_uri)
    mlflow_inst.sklearn.log_model(
        sk_model=best_pipeline,
        artifact_path="AutoML-model",
    )
    update_production_latest_model(
        client, mlflow_inst.active_run().info.run_id, experiment_name
    )
    mlflow_inst.log_artifacts(artifacts_path)
    mlflow_inst.end_run()


def archive_production_model(experiment_name, client=None):
    """Archives the model in production of a use-case.

    Parameters:
        client (): the mlflow client
        experiment_name (str): the use case name

    """

    if client is None:
        client = MlflowClient(tracking_uri="http://192.168.1.14:9431/")

    model_metadata = retrieve_production_model_metadata(experiment_name)

    client.transition_model_version_stage(
        name=model_metadata["model_name"],
        version=model_metadata["model_version"],
        stage="Archived",
    )


def update_production_latest_model(client, run_id, experiment_name):
    """

    Parameters:

    Returns:

    """
    model_uri = f"runs:/{run_id}/AutoML-model"
    mv = mlflow.register_model(model_uri, experiment_name + "_predictive-model")

    # if a previous model exists for this experiment, change its stage to archived
    if int(mv.version) > 1:
        client.transition_model_version_stage(
            name=mv.name, version=int(mv.version) - 1, stage="Archived"
        )

    # set the current model's stage to Production
    client.transition_model_version_stage(
        name=mv.name, version=mv.version, stage="Production"
    )
    return mv.version


def retrieve_production_model(experiment_name):
    """Get the model staged as 'Production' in a specific experiment

    Args:
        experiment_name (str): the use case name

    Returns:
        model (evalml.pipeline_model): The 'Production' staged model
    """

    # TODO: Set stage dynamically to retrieve any of the models
    stage = "Production"
    model_uri = f"models:/{experiment_name+'_'+'predictive-model'}/{stage}"
    try:
        model = mlflow.sklearn.load_model(model_uri=model_uri)
    except Exception as e:
        print(f"{e.__class__} Exception occured")
        print('No model available staged as "Production" for this use case')

    return model


def retrieve_production_model_metadata(experiment_name):
    """Get the artifact of the model staged as 'Production' in a specific experiment

    Args:
        experiment_name (str): the use case name

    Returns:
        model_metadata (dict): the artifact of the 'Production' staged model
    """

    client = MlflowClient(tracking_uri="http://192.168.1.14:9431/")
    experiment_runs = client.search_model_versions(
        f"name='{experiment_name}_predictive-model'"
    )
    artifact_location = None
    for mv in experiment_runs:
        if mv.current_stage == "Production":
            artifact_location = os.path.dirname(mv.source)
            break
    if artifact_location is not None:
        with open(artifact_location + "/train_artifacts.json", "r") as handle:
            model_metadata = json.load(handle)
    else:
        raise Exception("No trained model found for this use case.")

    return model_metadata
