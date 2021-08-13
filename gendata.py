import csv
import random


def generate_csv(file_name: str, col_name: [], rows: int, range_min: float, range_max: float):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(col_name)
        for i in range(rows):
            writer.writerow([i, random.uniform(range_min, range_max)])


if __name__ == '__main__':
    file_name = './data/data.csv'
    col_name = ['id', 'value']
    rows = 100
    range_min = 0.0
    range_max = 100.0
    generate_csv(file_name, col_name, rows, range_min, range_max)
