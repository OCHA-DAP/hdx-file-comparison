#!/usr/bin/env python
# encoding: utf-8

import csv
import difflib
import re


def difflib_compare(filepath_1: str, filepath_2: str, encoding: str = "utf-8") -> list[tuple]:
    diff = difflib.ndiff(
        open(filepath_1, encoding=encoding).read().splitlines(),
        open(filepath_2, encoding=encoding).read().splitlines(),
    )
    return [(i, x) for i, x in enumerate(diff) if x[0] in ["-", "+", "?"]]


def detect_cell_change_from_diff(header: list[str], diff: list[tuple]):
    cell_changes = []
    for i in range(0, len(diff) - 1):
        if diff[i][1].startswith("- ") and diff[i + 1][1].startswith("? "):
            print(diff[i], flush=True)
            print(diff[i + 1], flush=True)
            print(diff[i + 2], flush=True)
            print(diff[i + 3], flush=True)

            # Find index of carets

            idxs = [m.start() for m in re.finditer("\^", diff[i + 1][1])]
            print(idxs, flush=True)
            probe_row = list(diff[i][1])
            for idx in idxs:
                probe_row[idx] = "^"
            probe_row = "".join(probe_row)

            row = list(csv.reader([probe_row[2:]]))

            for j, column in enumerate(row[0]):
                if "^" in column:
                    original_row = list(csv.reader([diff[i][1][2:]]))[0]
                    new_row = list(csv.reader([diff[i + 2][1][2:]]))[0]
                    print(j, flush=True)
                    print(header, flush=True)
                    print(original_row, flush=True)
                    print(new_row, flush=True)
                    status = (
                        f"Column '{header[j]}' has been changed from "
                        f"'{original_row[j]}' to '{new_row[j]}' on row '{diff[i][0]}'"
                    )
                    print(status, flush=True)
                    cell_changes.append(status)

            # for row in rows:
            #     print(row, flush=True)

    return cell_changes


def process(filepath_1: str, filepath_2: str, encoding: str = "utf-8"):
    # Get headers
    headers = []
    with open(filepath_2, encoding=encoding) as file_handle:
        csv_reader = csv.reader(file_handle)

        headers = next(csv_reader)
    # Get diff
    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")

    # Process diff
    cell_changes = detect_cell_change_from_diff(headers, diff)

    return cell_changes
