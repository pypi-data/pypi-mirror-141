# TODO: Docstrings and turn this into a class
# TODO: This needs rework
import json
import os
import sys
import time

import pika
import psycopg2

from sphynxml.ETL.SphynxETL import SphynxETL
from sphynxml.Predictors.SphynxPredictor import SphynxPredictor
from sphynxml.Preprocessors.SphynxEncoder import SphynxEncoder
from sphynxml.Preprocessors.SphynxTransformer import SphynxTransformer

connection = psycopg2.connect(
    database="mldb",
    user="postgres",
    password="z(>uCysA`Z6>{E(W",
    hostaddr="195.201.62.2",
    host="localhost",
)


def callback(ch, method, properties, body):
    body_json = json.loads(body)
    print(" [x] Received %r" % body_json)
    return_queue = body_json["assessment_model_execution_id"]
    ch.queue_declare(queue=return_queue, durable=True)
    cursor = connection.cursor()
    sp = SphynxPredictor(body_json["workflowid"])
    st = SphynxTransformer()
    se = SphynxEncoder()

    query = (
        'SELECT "targetVariable","useCaseSpecificVariable" FROM "workflow" WHERE "id"'
        " = %s"
    )
    cursor.execute(query, (body_json["workflowid"],))
    query_result = cursor.fetchone()
    key_names = ["targetVariable", "useCaseSpecificVariable"]
    workflow_json = {
        key_name: entry for key_name, entry in zip(key_names, query_result)
    }

    workflow_json["predicted_variable_name"] = workflow_json["targetVariable"]
    workflow_json["origin"] = "elastic"

    load_task = SphynxETL()
    load_task.init_task(body_json)
    # TODO: Perform testing to guarantee 1 sample return and change size to 1 in this call
    data = load_task.load_data(split=False, size=10)

    if data.empty:
        prediction_results = -1
    else:
        data_to_predict = data.head(1)
        data_to_predict = st.data_transform(
            data_to_predict, drop_columns=False, list_to_str=True
        )
        data_to_predict = se.data_encode(data_to_predict)
        # TODO: Need to perform additional checks here and work with elastic because there could be missing
        # columns during data fetching
        try:
            print(data_to_predict["system:auth:ssh:signature"])
            print(data_to_predict["geo:region_iso_code"])
        except Exception as e:
            print(f"{e.__class__} Exception occured")
            data_to_predict["system:auth:ssh:signature"] = ""
            data_to_predict["geo:region_iso_code"] = ""
            print("Missing features in the test sample. Using default value ")
        prediction_results = sp.predict(data_to_predict)
        print(prediction_results)
        prediction_results = prediction_results["predictions_proba"][1].values.tolist()[
            0
        ]

    results = {
        "Id": "7",
        "type": "call",
        "sender": "MLtool",
        "receiver": "monitor",
        "arguments": [
            "ML_check_login",
            "_opInst",
            body_json["userName"],
            body_json["workflowid"],
            str(prediction_results),
        ],
        "time": int(round(time.time() * 1000)),
        "source": "MLtool",
    }
    print(results)
    ch.basic_publish(exchange="", routing_key=return_queue, body=json.dumps(results))


def main():

    # connect to monitor
    # context = ssl.create_default_context(
    # cafile="/home/mlearning/test/certs/monitor/ca_certificate.pem")
    # context.load_cert_chain(
    # "/home/mlearning/test/certs/monitor/client_certificate.pem",
    # "/home/mlearning/test/certs/monitor/client_key.pem"
    # )
    # ssl_options = pika.SSLOptions(context, '192.168.1.15')
    # conn_params = pika.ConnectionParameters(
    # port=5671,
    # ssl_options=ssl_options
    # )
    # credentials = pika.ExternalCredentials(
    # '/home/mlearning/test/certs/monitor/client_key.pem'
    # )
    # connection = pika.BlockingConnection(conn_params,credentials=credentials)

    # connect to localhost
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # connect to monitor
    credentials = pika.PlainCredentials("monitoradmin", "1m0n!t0rSTS#")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="195.201.62.2", port=5672, credentials=credentials
        )
    )

    print("Connected")
    channel = connection.channel()
    channel.exchange_declare(exchange="AssuranceToolNotifyML", exchange_type="topic")

    channel.queue_declare(queue="consumeAssuranceToolNotifications", durable=True)
    channel.queue_bind(
        exchange="AssuranceToolNotifyML", queue="consumeAssuranceToolNotifications"
    )
    channel.basic_consume(
        queue="consumeAssuranceToolNotifications",
        on_message_callback=callback,
        auto_ack=True,
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
