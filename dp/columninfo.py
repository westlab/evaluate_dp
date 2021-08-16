import pandas as pd
import yaml


class ColumnInfo:
    min: float
    max: float
    epsilon: float

    def __init__(self, min: float, max: float, epsilon: float):
        if min > max:
            raise ValueError(f'min must not be greater than max, but min {min}, max {max}')
        self.min = min
        self.max = max
        self.epsilon = epsilon

    def span(self) -> float:
        return self.max - self.min


def new_column_info_from_dict(conf: dict[str, any]) -> ColumnInfo:
    return ColumnInfo(conf['min'], conf['max'], conf['epsilon'])


def new_column_info_list_from_yaml(file_name: str) -> dict[str, ColumnInfo]:
    with open(file_name) as f:
        obj = yaml.safe_load(f)
    info_list: dict[str, ColumnInfo] = {}
    for k, val in obj['columns'].items():
        info_list[k] = new_column_info_from_dict(val)

    return info_list


if __name__ == '__main__':
    new_column_info_list_from_yaml('../data/conf.yaml')
