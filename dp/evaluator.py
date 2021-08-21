import datetime
import math
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .applyforplain import apply_for_plain
from .columninfo import ColumnInfo
from .dputil import NumberType, with_indent

PARAMS: List[str] = ["mean", "std"]
EPS: float = 1e-4


class DPEvaluator:
    data_frame: pd.DataFrame
    target_col: Dict[str, ColumnInfo]
    output_int: bool

    results = Dict[str, Dict[str, np.ndarray]]
    exp_params = Dict[str, Dict[str, Dict[str, NumberType]]]
    got_params = Dict[str, Dict[str, Dict[str, NumberType]]]

    def __init__(
        self,
        data_frame: pd.DataFrame,
        target_col: Dict[str, ColumnInfo],
        output_int: bool = False,
    ):
        self.data_frame = data_frame
        self.target_col = target_col
        self.results = {"mean": {}, "std": {}}
        self.exp_params = {"mean": {}, "std": {}}
        self.got_params = {"mean": {}, "std": {}}
        self.output_int = output_int

    def exec_dp(self, exec_times: int = 10000) -> None:
        n = len(self.data_frame.index)
        for col, val in self.target_col.items():
            epsilon = val.epsilon
            self.results["mean"][col] = np.array([])
            self.results["std"][col] = np.array([])
            span = val.span()
            l1_mean = span / n
            l1_std = span * math.sqrt(1.0 / n - 1.0 / n ** 2)
            if self.output_int:
                self.exp_params["mean"][col] = {
                    "mean": np.mean(self.data_frame[col]).astype(np.int64).item(),
                    "std": round(math.sqrt(2) * l1_mean / epsilon),
                }
                self.exp_params["std"][col] = {
                    "mean": np.std(self.data_frame[col]).astype(np.int64).item(),
                    "std": round(math.sqrt(2) * l1_std / epsilon),
                }
            else:
                self.exp_params["mean"][col] = {
                    "mean": np.mean(self.data_frame[col]),
                    "std": math.sqrt(2) * l1_mean / epsilon,
                }
                self.exp_params["std"][col] = {
                    "mean": np.std(self.data_frame[col]),
                    "std": math.sqrt(2) * l1_std / epsilon,
                }

        for i in range(exec_times):
            result = apply_for_plain(self.data_frame, self.target_col, self.output_int)
            for col in self.target_col.keys():
                self.results["mean"][col] = np.append(
                    self.results["mean"][col], result[col]["mean"]
                )
                self.results["std"][col] = np.append(
                    self.results["std"][col], result[col]["std"]
                )
        for col in self.target_col.keys():
            for param in PARAMS:
                if self.output_int:
                    self.got_params[param][col] = {
                        "mean": np.mean(self.results[param][col])
                        .astype(np.int64)
                        .item(),
                        "std": np.std(self.results[param][col]).astype(np.int64).item(),
                    }
                else:
                    self.got_params[param][col] = {
                        "mean": np.mean(self.results[param][col]),
                        "std": np.std(self.results[param][col]),
                    }

    def get_result(self) -> Dict[str, Dict[str, np.ndarray]]:
        return self.results

    def show_summary(self) -> None:
        for col in self.target_col.keys():
            print(f"{col}:")
            for param in PARAMS:
                print(with_indent(2, f"{param}:"))
                print(
                    with_indent(
                        4, f'actual value: {self.exp_params[param][col]["mean"]}'
                    )
                )
                print(with_indent(4, "values after DP:"))
                print(
                    with_indent(
                        8,
                        f"expected: {self.exp_params[param][col]}, got: {self.got_params[param][col]}",
                    )
                )

    def generate_histogram(self, param: str, col: str, output_path: str = "") -> str:
        if param not in PARAMS:
            raise ValueError(f"param {param} is unknown, support params {PARAMS}")
        if len(self.results["mean"]) == 0:
            print("DP has not be executed. Now start executing...")
            self.exec_dp()
            print("Executing DP process finished")

        op = output_path
        if op == "":
            op = f"histogram_{param}_{datetime.datetime.now().isoformat()}.png"

        target: np.ndarray = self.results[param][col]
        fig = plt.figure()
        plt.hist(self.results[param][col], 50, density=True)

        plotx = np.arange(target.min(), target.max(), 0.01)
        loc = self.exp_params[param][col]["mean"]
        scale = self.exp_params[param][col]["std"] / np.sqrt(2)
        pdf = np.exp(-abs(plotx - loc) / (scale + EPS)) / (2.0 * (scale + EPS))
        plt.plot(plotx, pdf)
        fig.savefig(output_path)
        return op
