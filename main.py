from dp.applyforplain import apply_for_plain

if __name__ == '__main__':
    file_name='./data/data.csv'
    epsilon = 0.2
    value_range=100.0
    ret = apply_for_plain(file_name, epsilon, {"value":100.0})
    print(ret)