# TODO: This needs rework
import random
from typing import Dict, List, Optional, Tuple, Union

import numpy as np


def reservoir_sampling(
    X_ref: np.ndarray, X: np.ndarray, reservoir_size: int, n: int
) -> np.ndarray:
    """
    Apply reservoir sampling.
    Parameters
    ----------
    X_ref
        Current instances in reservoir.
    X
        Data to update reservoir with.
    reservoir_size
        Size of reservoir.
    n
        Number of total instances that have passed so far.
    Returns
    -------
    Updated reservoir.
    """
    if X.shape[0] + n <= reservoir_size:
        return np.concatenate([X_ref, X], axis=0)

    n_ref = X_ref.shape[0]
    output_size = min(reservoir_size, n_ref + X.shape[0])
    shape = (output_size,) + X.shape[1:]
    X_reservoir = np.zeros(shape, dtype=X_ref.dtype)
    X_reservoir[:n_ref] = X_ref
    for item in X:
        n += 1
        if n_ref < reservoir_size:
            X_reservoir[n_ref, :] = item
            n_ref += 1
        else:
            r = int(random.random() * n)
            if r < reservoir_size:
                X_reservoir[r, :] = item
    return X_reservoir


def update_reference(
    X_ref: np.ndarray,
    X: np.ndarray,
    n: int,
    update_method: Dict[str, int] = None,
) -> np.ndarray:
    """
    Update reference dataset for drift detectors.
    Parameters
    ----------
    X_ref
        Current reference dataset.
    X
        New data.
    n
        Count of the total number of instances that have been used so far.
    update_method
        Dict with as key `reservoir_sampling` or `last` and as value n. `reservoir_sampling` will apply
        reservoir sampling with reservoir of size n while `last` will return (at most) the last n instances.
    Returns
    -------
    Updated reference dataset.
    """
    if isinstance(update_method, dict):
        update_type = list(update_method.keys())[0]
        size = update_method[update_type]
        if update_type == "reservoir_sampling":
            return reservoir_sampling(X_ref, X, size, n)
        elif update_type == "last":
            X_update = np.concatenate([X_ref, X], axis=0)
            return X_update[-size:]
        else:
            raise KeyError(
                "Only `reservoir_sampling` and `last` are valid update options for"
                " X_ref."
            )
    else:
        return X_ref


def get_input_shape(
    shape: Optional[Tuple], x_ref: Union[np.ndarray, list]
) -> Optional[Tuple]:
    """Optionally infer shape from reference data."""
    if isinstance(shape, tuple):
        return shape
    elif hasattr(x_ref, "shape"):
        return x_ref.shape[1:]
    else:
        raise TypeError("Input shape could not be inferred. ")
        return None


def fdr(p_val: np.ndarray, q_val: float) -> Tuple[int, Union[float, np.ndarray]]:
    """
    Checks the significance of univariate tests on each variable between 2 samples of
    multivariate data via the False Discovery Rate (FDR) correction of the p-values.
    Parameters
    ----------
    p_val
        p-values for each univariate test.
    q_val
        Acceptable q-value threshold.
    Returns
    -------
    Whether any of the p-values are significant after the FDR correction
    and the max threshold value or array of potential thresholds if no p-values
    are significant.
    """
    n = p_val.shape[0]
    i = np.arange(n) + 1
    p_sorted = np.sort(p_val)
    q_threshold = q_val * i / n
    below_threshold = p_sorted < q_threshold
    try:
        idx_threshold = np.where(below_threshold)[0].max()
    except ValueError:  # sorted p-values not below thresholds
        return int(below_threshold.any()), q_threshold
    return int(below_threshold.any()), q_threshold[idx_threshold]


def _get_counts(
    x: np.ndarray, categories: Dict[int, List[int]]
) -> Dict[int, List[int]]:
    """
    Utility method for getting the counts of categories for each categorical variable.
    """
    return {f: [(x[:, f] == v).sum() for v in vals] for f, vals in categories.items()}
