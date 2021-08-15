import datetime
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .applyforplain import apply_for_plain
from .columninfo import ColumnInfo
from .dputil import with_indent

PARAMS: list[str] = ['mean', 'std']


class DPEvaluator:
    data_frame: pd.DataFrame
    epsilon: float
    target_col: dict[str, ColumnInfo]

    results = dict[str, dict[str, np.ndarray]]
    exp_params = dict[str, dict[str, dict[str, float]]]
    got_params = dict[str, dict[str, dict[str, float]]]

    def __init__(self, data_frame: pd.DataFrame, epsilon: float, target_col: dict[str, ColumnInfo]):
        self.data_frame = data_frame
        self.epsilon = epsilon
        self.target_col = target_col
        self.results = {'mean': {}, 'std': {}}
        self.exp_params = {'mean': {}, 'std': {}}
        self.got_params = {'mean': {}, 'std': {}}

    def exec_dp(self, exec_times: int = 10000) -> None:
        n = len(self.data_frame.index)
        for col, val in self.target_col.items():
            self.results['mean'][col] = np.array([])
            self.results['std'][col] = np.array([])
            span = val.span()
            l1_mean = span / n
            l1_std = span * math.sqrt(1.0 / n - 1.0 / n ** 2)
            self.exp_params['mean'][col] = {'mean': np.mean(self.data_frame[col]),
                                            'std': math.sqrt(2) * l1_mean / self.epsilon}
            self.exp_params['std'][col] = {'mean': np.std(self.data_frame[col]),
                                           'std': math.sqrt(2) * l1_std / self.epsilon}

        for i in range(exec_times):
            result = apply_for_plain(self.data_frame, self.epsilon, self.target_col)
            for col in self.target_col.keys():
                self.results['mean'][col] = np.append(self.results['mean'][col], result[col]['mean'])
                self.results['std'][col] = np.append(self.results['std'][col], result[col]['std'])
        for col in self.target_col.keys():
            for param in PARAMS:
                self.got_params[param][col] = {'mean': np.mean(self.results[param][col]),
                                               'std': np.std(self.results[param][col])}

    def get_result(self) -> dict[str, dict[str, np.ndarray]]:
        return self.results

    def show_summary(self) -> None:
        for col in self.target_col.keys():
            print(f"{col}:")
            for param in PARAMS:
                print(with_indent(2, f'{param}:'))
                print(with_indent(4, f'actual value: {self.exp_params[param][col]["mean"]}'))
                print(with_indent(4, f'values after DP:'))
                print(with_indent(8, f'expected: {self.exp_params[param][col]}, got: {self.got_params[param][col]}'))

    def generate_histogram(self, param: str, col: str, output_path: str = '') -> str:
        if param not in PARAMS:
            raise ValueError(f'param {param} is unknown, support params {PARAMS}')
        if len(self.results['mean']) == 0:
            print('DP has not be executed. Now start executing...')
            self.exec_dp()
            print('Executing DP process finished')

        op = output_path
        if op == '':
            op = f'histogram_{param}_{datetime.datetime.now().isoformat()}.png'

        target: np.ndarray = self.results[param][col]
        fig = plt.figure()
        plt.hist(self.results[param][col], 50, density=True)

        plotx = np.arange(target.min(), target.max(), 0.01)
        loc = self.exp_params[param][col]['mean']
        scale = self.exp_params[param][col]['std'] / np.sqrt(2)
        pdf = np.exp(-abs(plotx - loc) / scale) / (2.0 * scale)
        plt.plot(plotx, pdf)
        fig.savefig(output_path)
        return op
