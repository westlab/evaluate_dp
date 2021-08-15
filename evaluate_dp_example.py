import pandas as pd

from dp.evaluator import DPEvaluator
from dp.columninfo import ColumnInfo

if __name__ == '__main__':
    input_file = './data/data.csv'
    df = pd.read_csv(input_file)
    epsilon = 3.0
    target_col = {'value': ColumnInfo(0.0, 100.0)}
    evaluator = DPEvaluator(df, epsilon, target_col)
    evaluator.exec_dp(10000)
    evaluator.show_summary()
    result = evaluator.get_result()
    evaluator.generate_histogram('std', 'value', './data/tmp_std.png')
    evaluator.generate_histogram('mean', 'value', './data/tmp_mean.png')
