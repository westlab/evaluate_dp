from typing import Any, Dict, Optional, Union

import pandas as pd

from .applyforplain import apply_for_plain, generate_noise_by_column
from .columninfo import (
    ColumnInfo,
    new_column_info_list_from_dict,
    new_column_info_list_from_yaml,
)
from .dputil import NumberType
from .evaluator import DPEvaluator


class Table:
    data: pd.DataFrame
    dp_conf: Dict[str, ColumnInfo]
    output_int: bool

    def __init__(
        self,
        data_frame: pd.DataFrame,
        dp_conf: Dict[str, ColumnInfo],
        output_int: bool = False,
    ):
        self.data = data_frame
        self.dp_conf = dp_conf
        self.output_int = output_int

    def apply_dp(self) -> Dict[str, Dict[str, NumberType]]:
        return apply_for_plain(self.data, self.dp_conf, self.output_int)

    def create_evaluator(self) -> DPEvaluator:
        return DPEvaluator(self.data, self.dp_conf, self.output_int)

    def generate_noise(
        self, col: str, stat_name: Optional[str] = None
    ) -> Union[NumberType, Dict[str, NumberType]]:
        n = len(self.data[col])
        info = self.dp_conf[col]
        result = generate_noise_by_column(n, info, self.output_int)
        if stat_name is not None:
            return result[stat_name]
        return result


def new_table_from_yaml(
    data_frame: pd.DataFrame, conf_file: str, output_int: bool = False
) -> Table:
    conf = new_column_info_list_from_yaml(conf_file, output_int)
    return Table(data_frame, conf, output_int)


def new_table_from_dict(
    data_frame: pd.DataFrame, conf_dict: Dict[str, Any], output_int: bool = False
) -> Table:
    conf = new_column_info_list_from_dict(conf_dict, output_int)
    return Table(data_frame, conf, output_int)
