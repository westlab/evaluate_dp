from typing import Dict

import yaml

from .dputil import NumberType


class ColumnInfo:
    min: NumberType
    max: NumberType
    epsilon: NumberType

    def __init__(self, min: NumberType, max: NumberType, epsilon: NumberType):
        if min > max:
            raise ValueError(
                f"min must not be greater than max, but min {min}, max {max}"
            )
        self.min = min
        self.max = max
        self.epsilon = epsilon

    def span(self) -> NumberType:
        return self.max - self.min


def new_column_info_from_dict(
    conf: Dict[str, NumberType], output_int: bool = False
) -> ColumnInfo:
    if output_int:
        return ColumnInfo(int(conf["min"]), int(conf["max"]), int(conf["epsilon"]))
    else:
        return ColumnInfo(conf["min"], conf["max"], conf["epsilon"])


def new_column_info_list_from_yaml(
    file_name: str, output_int: bool = False
) -> Dict[str, ColumnInfo]:
    with open(file_name) as f:
        obj = yaml.safe_load(f)
    info_list: Dict[str, ColumnInfo] = {}
    for k, val in obj["columns"].items():
        info_list[k] = new_column_info_from_dict(val, output_int)
    return info_list
