class ColumnInfo:
    min: float
    max: float

    def __init__(self, min: float, max: float):
        if min > max:
            raise ValueError(f'min must not be greater than max, but min {min}, max {max}')
        self.min = min
        self.max = max

    def span(self) -> float:
        return self.max - self.min
