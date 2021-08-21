from typing import Dict

import pandas as pd

from .applyforplain import apply_for_plain
from .columninfo import ColumnInfo, new_column_info_list_from_yaml
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


def new_table_from_yaml(
    data_frame: pd.DataFrame, conf_file: str, output_int: bool = False
) -> Table:
    conf = new_column_info_list_from_yaml(conf_file, output_int)
    return Table(data_frame, conf, output_int)
