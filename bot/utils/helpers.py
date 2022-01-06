import inspect
from typing import Any


def find_nth_occurrence(string: str, substring: str, n: int) -> int | None:
    """Return index of `n`th occurrence of `substring` in `string`, or None if not found."""
    index = 0
    for _ in range(n):
        index = string.find(substring, index + 1)
        if index == -1:
            return None
    return index


def get_class_attributes(cls) -> list[tuple]:
    """Gets all non-dunder sttributes of a class, excluding methods."""
    attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
    return [
        a for a in attributes if not (a[0].startswith("__") and a[0].endswith("__"))
    ]
