from typing import Union, Type

NumberType: Type = Union[int, float]


def with_indent(indent: int, string: str) -> str:
    return f"{' ' * indent}{string}"
