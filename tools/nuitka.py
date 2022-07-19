"""
Nuitka Compilation Draft
"""
from typing import Union


def kwargs_flat(kwarg: str, _list: Union[list, filter, map]):
    counter = 0
    for i in range(len(_list) * 2):
        if (i % 2) != 0:
            yield _list[counter]
            counter += 1
            continue
        yield kwarg


GENERAL = [
    *(
        "--standalone",
        "--warn-implicit-exceptions",
        "--warn-unusual-code",
        "--assume-yes-for-downloads",
    ),
    *kwargs_flat("--python-flag=", ["no_asserts", "no_docstrings"]),
]

CMD = [*GENERAL]

print("python -m nuitka " + " ".join(CMD), end="")
