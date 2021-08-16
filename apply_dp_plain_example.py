import numpy as np
import pandas as pd

from dp.applyforplain import apply_for_plain
from dp.columninfo import ColumnInfo

if __name__ == '__main__':
    file_name = './data/data.csv'
    df = pd.read_csv(file_name)
    value_range = 100.0
    target_col = {'value': ColumnInfo(0.0, 100.0, 3.0)}
    print(np.mean(df['value']))
    ret = apply_for_plain(df, target_col)
    print(ret)
