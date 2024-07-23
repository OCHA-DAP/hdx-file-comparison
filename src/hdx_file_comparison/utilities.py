#!/usr/bin/env python
# encoding: utf-8

import difflib


def difflib_compare(filepath_1: str, filepath_2: str, encoding: str = "utf-8") -> list[str]:
    diff = difflib.ndiff(
        open(filepath_1, encoding=encoding).read().splitlines(),
        open(filepath_2, encoding=encoding).read().splitlines(),
    )
    return [x for x in diff if x[0] in ["-", "+", "?"]]
