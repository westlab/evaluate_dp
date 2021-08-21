from typing import Union

NumberType = Union[int, float]


def with_indent(indent: int, string: str) -> str:
    return f"{' ' * indent}{string}"
