import math

import numpy as np
import pandas as pd

_rng = np.random.default_rng()


def generate_noise(epsilon: float, l1_sensitive: float):
    lam = l1_sensitive / epsilon
    r = _rng.laplace(0, lam, 1)
    return float(r[0])


def apply_for_plain(data_frame: pd.DataFrame, epsilon: float, value_range: dict[str, float]) \
        -> dict[str, dict[str, float]]:
    df = data_frame.copy()
    n = len(df.index)
    result = {}
    for col, vr in value_range.items():
        l1_mean = vr / n
        l1_std = vr * math.sqrt(1.0 / n - 1.0 / n ** 2)
        mean_dp = np.mean(df[col]) + generate_noise(epsilon, l1_mean)
        std_dp = np.std(df[col]) + generate_noise(epsilon, l1_std)
        result[col] = {"mean": mean_dp, "std": std_dp}

    return result
