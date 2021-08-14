import numpy as np
import pandas as pd

from dp.applyforplain import apply_for_plain

if __name__ == '__main__':
    file_name = './data/data.csv'
    df = pd.read_csv(file_name)
    epsilon = 0.2
    value_range = 100.0
    print(np.mean(df['value']))
    ret = apply_for_plain(df, epsilon, {"value": 100.0})
    print(ret)
