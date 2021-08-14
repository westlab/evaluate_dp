import datetime
import math

import numpy as np
import pandas as pd

from applyforplain import apply_for_plain


def show_summary():
    # TODO:　分布結果の表示
    pass


def apply_dp_iter(data_frame: pd.DataFrame, epsilon: float, target_col: dict[str, float],
                  generate_times: int = 100000, is_output_histogram: bool = False, output_path: str = '') \
        -> (dict[str, np.array], dict[str, np.array]):
    result_mean = {}
    result_std = {}
    exp_mean_dist = {}
    exp_std_dist = {}
    n = len(data_frame.index)
    for col, val in target_col:
        result_mean[col] = np.array([])
        result_std[col] = np.array([])
        l1_mean = val / n
        l1_std = val * math.sqrt(1.0 / n - 1.0 / n ** 2)
        exp_mean_dist[col] = {'mean': np.mean(data_frame[col]), 'std': math.sqrt(2) * l1_mean / epsilon}
        exp_std_dist[col] = {'mean': np.std(data_frame[col]), 'std': math.sqrt(2) * l1_std / epsilon}

    for i in range(generate_times):
        result = apply_for_plain(data_frame, epsilon, target_col)
        for col in target_col.keys():
            result_mean[col] = np.append(result_mean[col], result[col]['mean'])
            result_std[col] = np.append(result_std[col], result[col]['std'])

    if is_output_histogram:
        op = output_path
        if op == '':
            op = f'histogram_{datetime.datetime.now().isoformat()}.png'

    return result_mean, result_std


def validate_dp_plain(data_frame: pd.DataFrame, epsilon: float, target_col: dict[str, float],
                      generate_times: int = 100000):
    pass
