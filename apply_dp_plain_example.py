import numpy as np
import pandas as pd

from dp.applyforplain import apply_for_plain
from dp.columninfo import ColumnInfo
from dp.table import new_table_from_yaml

if __name__ == '__main__':
    file_name = './data/data.csv'
    conf_file = './data/conf.yaml'
    df = pd.read_csv(file_name)
    table = new_table_from_yaml(df, conf_file)
    ret = table.apply_dp()
    print(ret)
