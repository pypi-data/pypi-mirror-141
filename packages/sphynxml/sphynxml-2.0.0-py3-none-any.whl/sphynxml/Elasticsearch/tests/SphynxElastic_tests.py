import logging
from typing import Dict


def _check_connection(es):

    if es.ping():
        return True

    return False


def _check_true_value(dic: Dict, size: int):
    """Checks if the returned number of values from the elastic is equal
    to the expected returned values.

    Parameters:
            dic (dictionary): the returned values
            size (int): the maximum number of values to query

    """

    ret_value = dic["hits"]["total"]["value"]
    true_value = len(dic["hits"]["hits"])

    if size > true_value and ret_value != true_value:
        logging.error("Query failed.")
        # TODO: raise error

    return
