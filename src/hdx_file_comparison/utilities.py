#!/usr/bin/env python
# encoding: utf-8

import csv
import difflib
import re

from hdx_file_comparison.time_limiter import run_with_timer, TimeExceededException

MAX_EXECUTION_TIME = 20


def difflib_compare(filepath_1: str, filepath_2: str, encoding: str = "utf-8") -> list[tuple]:
    diff = difflib.ndiff(
        open(filepath_1, encoding=encoding).read().splitlines(),
        open(filepath_2, encoding=encoding).read().splitlines(),
    )
    return [(i, x) for i, x in enumerate(diff) if x[0] in ["-", "+", "?"]]


def difflib_column_changes(filepath_1: str, filepath_2: str, encoding: str = "utf-8"):
    column_diffs = {}
    with open(filepath_1, encoding=encoding) as filepath_1_handle:
        file_1_rows = list(csv.DictReader(filepath_1_handle))

    with open(filepath_2, encoding=encoding) as filepath_2_handle:
        file_2_rows = list(csv.DictReader(filepath_2_handle))

    columns = list(file_1_rows[0].keys())

    print(columns, flush=True)

    for column in columns:
        try:
            column_changes = process_column(file_1_rows, file_2_rows, column)
            column_diffs[column] = column_changes
        except TimeExceededException:
            print(
                f"Processing column '{column}' exceeded the maximum processing time of "
                f"{MAX_EXECUTION_TIME} seconds",
                flush=True,
            )
            column_diffs[column] = None

    return column_diffs


@run_with_timer(max_execution_time=MAX_EXECUTION_TIME)
def process_column(file_1_rows, file_2_rows, column):
    n_items = 650
    file_1_column = [x[column] for x in file_1_rows]
    file_2_column = [x[column] for x in file_2_rows]
    column_diff = difflib.ndiff(
        file_1_column[0:n_items],
        file_2_column[0:n_items],
    )
    column_changes = [(i, x) for i, x in enumerate(column_diff) if x[0] in ["-", "+", "?"]]
    return column_changes


def detect_cell_change_from_diff(header: list[str], diff: list[tuple]):
    cell_changes = []
    for i in range(0, len(diff) - 1):
        if diff[i][1].startswith("- ") and diff[i + 1][1].startswith("? "):
            print(diff[i], flush=True)
            print(diff[i + 1], flush=True)
            print(diff[i + 2], flush=True)
            print(diff[i + 3], flush=True)

            # Make a probe row which has the diff ^ characters added
            idxs = [m.start() for m in re.finditer("\^", diff[i + 1][1])]
            print(idxs, flush=True)
            probe_row = list(diff[i][1])
            for idx in idxs:
                probe_row[idx] = "^"
            probe_row = "".join(probe_row)
            row = list(csv.reader([probe_row[2:]]))

            # Check each column in the probe row for the ^ character
            for j, column in enumerate(row[0]):
                if "^" in column:
                    original_row = list(csv.reader([diff[i][1][2:]]))[0]
                    new_row = list(csv.reader([diff[i + 2][1][2:]]))[0]
                    status = (
                        f"Column '{header[j]}' has been changed from "
                        f"'{original_row[j]}' to '{new_row[j]}' on row '{diff[i][0]}'"
                    )
                    print(status, flush=True)
                    cell_changes.append(
                        {
                            "row": diff[i][0],
                            "column": header[j],
                            "original_value": original_row[j],
                            "new_value": new_row[j],
                        }
                    )

    return cell_changes


def compute_diff_metrics(diff: list[tuple]):
    diff_metrics = {}
    diff_metrics["n_lines_changed"] = int(sum([1 for x in diff if x[1].startswith("? ")]) / 2)
    diff_metrics["n_lines_added"] = int(
        sum([1 for x in diff if x[1].startswith("+ ")]) - diff_metrics["n_lines_changed"]
    )
    diff_metrics["n_lines_removed"] = int(
        sum([1 for x in diff if x[1].startswith("- ")]) - diff_metrics["n_lines_changed"]
    )

    return diff_metrics


def process(filepath_1: str, filepath_2: str, encoding: str = "utf-8"):
    # Get headers
    headers = []
    with open(filepath_2, encoding=encoding) as file_handle:
        csv_reader = csv.reader(file_handle)
        headers = next(csv_reader)
    # Get diff
    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")

    # Process diff
    diff_metrics = compute_diff_metrics(diff)
    diff_metrics["cell_changes"] = detect_cell_change_from_diff(headers, diff)

    return diff_metrics
