# TODO: This needs rework or drop
from SphynxML.Elasticsearch.SphynxElastic import SphynxElastic
from SphynxML.Preprocessors.SphynxEncoder import SphynxEncoder
from SphynxML.Preprocessors.SphynxFilterer import SphynxFilterer
from SphynxML.Preprocessors.SphynxTransformer import SphynxTransformer


def preprocessors_elastic_init():
    """
    Init the required modules for data loading and preprocessing.

    Returns:
        sphynxelastic, transformer, encoder, filter objects
    """

    selastic = SphynxElastic()
    stransformer = SphynxTransformer()
    sencoder = SphynxEncoder()
    sfilter = SphynxFilterer()
    selastic.connect()

    return selastic, stransformer, sencoder, sfilter


# def perform_model_performance_check(body_json):
# """
# TODO: Implement the logic once monitor defines the data loading technique
# """

# pass


# def perform_data_validity_check(body_json):
# """
# Perform a data validity check on requested data. Log this validity model to mlflow.
# If the invalid data are linked to a model, the model is also invalidated.

# Parameters:
# body_json (dict): A dictionary containing all the task metadata
# """

# # init the elk, tranformer, encoder and filter
# elk, st, se, sf = preproc_elk_init()

# #TODO: add the task_request logic in this script
# #TODO: Add the uc_compromise special handle
# elk_data = elk.query_field("event.action", "ssh_login")
# ids = elk_data["_id"]
# model_metadata = retrieve_production_model_metadata(body_json["use_case_id"])
# test_indeces = set(ids.values) - set(model_metadata["train_indeces"])
# if len(test_indeces) > 0:
# train_data = elk_data[elk_data["_id"].isin(model_metadata["train_indeces"])]
# train_data = train_data.drop(columns="_id", axis=1)
# train_data = st.data_transform(train_data)
# train_data = se.data_encoder(train_data)
# test_data = elk_data[elk_data["_id"].isin(test_indeces)]
# test_data = test_data.drop(columns="_id", axis=1)
# test_data = st.data_transform(test_data)
# test_data = se.data_encoder(test_data)

# train_data = train_data[model_metadata["included_data_features"]]
# test_data = test_data[model_metadata["included_data_features"]]
# # test_data = test_data[production_model_metadata['included_data_features']]

# smodel = SphynxValidator(
# use_case=body_json["use_case_id"],
# data_origin=body_json['train_data_origin']
# )
# drift_detected_flag = smodel.data_drift_check(
# train_data,
# test_data,
# ref_data_indeces=model_metadata["train_indeces"],
# test_data_indeces=list(test_indeces),
# )
# print(drift_detected_flag)
# # drift_detected_flag=1
# if drift_detected_flag:
# archive_production_model(smodel.client, body_json["use_case_id"])

# #TODO: Replace the placeholder result with what must be sent to the monitor
# result = {"time": time.time()}

# return result


# def perform_statistics_train(body_json):
# """
# Create a predictive model for a given use case. Set it to 'Production' stage.
# Archive the previously active model.

# Parameters:
# body_json (dict): A dictionary containing all the task metadata

# Returns:
# results_dict (dict): Dictionary containing the prediction results to be sent to
# monitor
# """

# # load the train data indeces used for the model training
# elk, st, se, sf = preproc_elk_init()

# #TODO: add the task_request logic in this script
# #TODO: Add the uc_compromise special handle
# ss = SphynxStatistics(use_case=body_json["use_case_id"])
# elk_data = elk.query_field("event.action", "ssh_login")
# ids = elk_data["_id"]
# elk_data = st.data_transform(elk_data)
# elk_data = elk_data.drop(columns="_id", axis=1)
# elk_data = se.data_encoder(elk_data)
# stat_result = ss.fit_statistics("summary", elk_data)
# print(stat_result)

# #TODO: Replace the placeholder result with what must be sent to the monitor
# result = {"time": time.time()}
# return result

# def perform_predictive_train_predict(body_json):
# # check train samples
# # retrain if different
# # predict if not
# pass


# def perform_predictive_train(body_json):
# """
# Create a predictive model for a given use case. Set it to 'Production' stage.
# Archive the previously active model.

# Parameters:
# body_json (dict): A dictionary containing all the task metadata

# Returns:
# results_dict (dict): Dictionary containing the prediction results to be sent to
# monitor
# """

# # init the elk, tranformer, encoder and filter
# elk, st, se, sf = preproc_elk_init()

# #TODO: add the task_request logic in this script
# #TODO: Add the uc_compromise special handle
# if 'uc_compromise' in body_json['use_case_id']:
# task_specific_vars = body_json['task_specific_variables']
# target_variable = body_json['predicted_variable_name']
# #target_variable = "_source:related:user"
# # this must be replaced with a single call
# elk_data = elk.query_field("event.action", "ssh_login")
# ids = elk_data["_id"]
# elk_data = elk_data.drop(columns="_id", axis=1)
# #elk_data[target_variable] = st.list_to_str(elk_data[target_variable])
# elk_data = st.data_transform(elk_data)
# elk_data[target_variable] = se.one_vs_all(
# elk_data[target_variable],
# task_specific_vars['user_id']
# )
# target = elk_data[target_variable]
# elk_data = se.data_encoder(elk_data)

# # this will be deleted
# elk_data = pd.concat([ids, elk_data], axis=1)
# train_data, _, train_target, _ = train_test_split(
# elk_data, target, test_size=0.3, stratify=target
# )
# train_indeces = train_data["_id"].values.tolist()
# train_data = sf.data_filter(train_data)

# # detect problem type from target variable
# problem_type = str(detect_problem_type(train_target))
# print(f"rabbitmq {problem_type}")

# if not (problem_type in ["binary", "regression"]):
# raise ValueError("Problem type not currently supported")

# model_hyperparams = body_json['model_hyperparams']
# print(model_hyperparams)
# smodel = SphynxPredictor(use_case=body_json["use_case_id"])

# smodel.fit(
# train_data=train_data,
# train_target=train_target,
# train_data_indeces=train_indeces,
# problem_type=problem_type,
# max_time=60,
# verbose=False,
# )

# #TODO: Replace the placeholder result with what must be sent to the monitor
# result = {"time": time.time()}
# return result


# def perform_predictive_predict(body_json):
# """
# Use a registered model labeled at 'Production' stage to make predictions on samples.
# If used in a use case with no valid models, throws an Exception.

# Parameters:
# body_json (dict): A dictionary containing all the task metadata

# Returns:
# results_dict (dict): Dictionary containing the prediction results to be sent to
# monitor
# """

# # init the elk, tranformer, encoder and filter
# elk, st, se, sf = preproc_elk_init()

# #TODO: add the task_request logic in this script
# #TODO: Add the uc_compromise special handle
# elk_data = elk.query_field("event.action", "ssh_login")
# ids = elk_data["_id"]
# model_metadata = retrieve_production_model_metadata(body_json["use_case_id"])
# test_indeces = set(ids.values) - set(model_metadata["train_indeces"])
# if len(test_indeces) > 0:
# test_dataset = elk_data[elk_data["_id"].isin(test_indeces)]
# test_dataset = st.data_transform(test_dataset)
# test_dataset = test_dataset.drop(columns="_id", axis=1)
# target_variable = "_source:related:user"
# test_dataset[target_variable] = se.one_vs_all(
# test_dataset[target_variable], "kalogiannis"
# )
# target = test_dataset[target_variable]
# test_dataset = se.data_encoder(test_dataset)
# test_dataset = test_dataset[model_metadata["included_data_features"]]
# smodel = SphynxPredictor(use_case=body_json["use_case_id"])
# predictions = smodel.predict(test_dataset)

# #TODO: Replace the placeholder result with what must be sent to the monitor
# result = {"time": time.time()}
# return result


# def perform_predictive_score(body_json):
# """
# Use a registered model labeled at 'Production' stage to score its performance on
# samples. If used in a use case with no valid models, throws an Exception.

# Parameters:
# body_json (dict): A dictionary containing all the task metadata

# Returns:
# results_dict (dict): Dictionary containing the score results to be sent to
# monitor
# """

# # init the elk, tranformer, encoder and filter
# elk, st, se, sf = preproc_elk_init()

# #TODO: add the task_request logic in this script
# #TODO: Add the uc_compromise special handle
# elk_data = elk.query_field("event.action", "ssh_login")
# target_variable = "_source:related:user"
# ids = elk_data["_id"]
# elk_data = st.data_transform(elk_data)
# elk_data[target_variable] = se.one_vs_all(elk_data[target_variable], "kalogiannis")
# model_metadata = retrieve_production_model_metadata(body_json["use_case_id"])
# test_indeces = set(ids.values) - set(model_metadata["train_indeces"])
# sp = SphynxPredictor(use_case=body_json["use_case_id"])
# if len(test_indeces) > 0:
# test_data = elk_data[elk_data["_id"].isin(test_indeces)]
# test_target = test_data[target_variable]
# test_data = se.data_encoder(test_data)
# test_data = test_data[model_metadata["included_data_features"]]
# prediction_results = sp.predict(test_data)
# print(test_target.value_counts())
# print(prediction_results["predictions"].value_counts())

# scores_results = sp.score(test_target, prediction_results["predictions"])
# print(scores_results)

# #TODO: Replace the placeholder result with what must be sent to the monitor
# result = {"time": time.time()}
# return result
