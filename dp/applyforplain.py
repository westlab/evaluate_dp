import math
from typing import Dict

import numpy as np
import pandas as pd

from .columninfo import ColumnInfo
from .dputil import NumberType

_rng = np.random.default_rng()


def generate_noise(epsilon: float, l1_sensitive: float) -> float:
    lam = l1_sensitive / epsilon
    r = _rng.laplace(0, lam, 1)
    return float(r[0])


def apply_for_plain(
    data_frame: pd.DataFrame,
    value_range: Dict[str, ColumnInfo],
    output_int: bool = False,
) -> Dict[str, Dict[str, NumberType]]:
    n = len(data_frame.index)
    result = {}
    for col, vr in value_range.items():
        epsilon = vr.epsilon
        span = vr.span()
        l1_mean = span / n
        l1_std = span * math.sqrt(1.0 / n - 1.0 / n ** 2)
        mean_dp = np.mean(data_frame[col]) + generate_noise(epsilon, l1_mean)
        std_dp = np.std(data_frame[col]) + generate_noise(epsilon, l1_std)
        if output_int:
            result[col] = {"mean": int(mean_dp), "std": int(std_dp)}
        else:
            result[col] = {"mean": mean_dp, "std": std_dp}

    return result
