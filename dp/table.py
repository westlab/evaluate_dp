import pandas as pd

from .columninfo import ColumnInfo, new_column_info_list_from_yaml
from .applyforplain import apply_for_plain
from .evaluator import DPEvaluator


class Table:
    data: pd.DataFrame
    dp_conf: dict[str, ColumnInfo]

    def __init__(self, data_frame: pd.DataFrame, dp_conf: dict[str, ColumnInfo]):
        self.data = data_frame
        self.dp_conf = dp_conf

    def apply_dp(self) -> dict[str, dict[str, float]]:
        return apply_for_plain(self.data, self.dp_conf)

    def create_evaluator(self) -> DPEvaluator:
        return DPEvaluator(self.data, self.dp_conf)


def new_table_from_yaml(data_frame: pd.DataFrame, conf_file: str) -> Table:
    conf = new_column_info_list_from_yaml(conf_file)
    return Table(data_frame, conf)
