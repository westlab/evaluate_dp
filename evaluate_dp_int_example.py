import pandas as pd

from dp.table import new_table_from_yaml

if __name__ == '__main__':
    input_file = './data/data_int.csv'
    conf_file = './data/conf_int.yaml'
    df = pd.read_csv(input_file)
    table = new_table_from_yaml(df, conf_file, output_int=True)
    evaluator = table.create_evaluator()
    evaluator.exec_dp(10000)
    evaluator.show_summary()
    print(evaluator.get_result())
    evaluator.generate_histogram('std', 'value', './data/tmp_std.png')
    evaluator.generate_histogram('mean', 'value', './data/tmp_mean.png')
