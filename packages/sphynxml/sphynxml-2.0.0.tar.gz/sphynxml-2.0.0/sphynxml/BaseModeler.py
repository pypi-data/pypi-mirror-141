import copy
from abc import ABC
from typing import Dict

DEFAULT_META = {
    "name": None,
    "modeler_type": None,  # predictive, statistical, preprocessing, interpretability, ETL
    "data_type": None,  # tabular, time-series
}


def outlier_prediction_dict():
    data = {"instance_score": None, "feature_score": None, "is_outlier": None}
    return copy.deepcopy({"data": data, "meta": DEFAULT_META})


def adversarial_prediction_dict():
    data = {"instance_score": None, "is_adversarial": None}
    return copy.deepcopy({"data": data, "meta": DEFAULT_META})


def adversarial_correction_dict():
    data = {
        "instance_score": None,
        "is_adversarial": None,
        "corrected": None,
        "no_defense": None,
        "defense": None,
    }
    return copy.deepcopy({"data": data, "meta": DEFAULT_META})


def concept_drift_dict():
    data = {"is_drift": None, "distance": None, "p_val": None, "threshold": None}
    return copy.deepcopy({"data": data, "meta": DEFAULT_META})


class BaseModeler(ABC):
    """Base class for Sphynx ML models."""

    def __init__(self):
        self.meta = copy.deepcopy(DEFAULT_META)
        self.meta["name"] = self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    @property
    def meta(self) -> Dict:
        return self._meta

    @meta.setter
    def meta(self, value: Dict):
        if not isinstance(value, dict):
            raise TypeError("meta must be a dictionary")
        self._meta = value
