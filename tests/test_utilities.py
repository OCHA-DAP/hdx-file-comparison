#!/usr/bin/env python
# encoding: utf-8

import os
import time
from hdx_file_comparison.utilities import difflib_compare, process, compute_diff_metrics

FIXTURES_DIRECTORY = os.path.join(os.path.dirname(__file__), "fixtures")
SMALL_FILE_ORIGINAL = os.path.join(FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg_qc.csv")
# Manually removed lines from start and end, and mutated a value
SMALL_FILE_CHANGED = os.path.join(
    FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg_qc_changed.csv"
)
BIG_FILE_ORIGINAL = os.path.join(FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg.csv")
# Manually removed lines from start and end, and mutated a value
BIG_FILE_CHANGED = os.path.join(FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg_changed.csv")


def test_difflib_compare_small():
    t0 = time.time()
    diff = difflib_compare(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    diff_metrics = compute_diff_metrics(diff)
    for row in diff:
        print(row, flush=True)

    assert diff_metrics["n_lines_changed"] == 1
    assert diff_metrics["n_lines_removed"] == 9
    assert diff_metrics["n_lines_added"] == 0


def test_difflib_compare_big():
    t0 = time.time()
    diff = difflib_compare(BIG_FILE_ORIGINAL, BIG_FILE_CHANGED, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    diff_metrics = compute_diff_metrics(diff)
    for row in diff:
        print(row, flush=True)

    assert diff_metrics["n_lines_changed"] == 1
    assert diff_metrics["n_lines_removed"] == 10
    assert diff_metrics["n_lines_added"] == 0


def test_process():
    t0 = time.time()
    cell_changes = process(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED)
    print(f"Process took {time.time()-t0:0.3f} seconds", flush=True)

    assert cell_changes == [
        "Column 'usdprice' has been changed from '0.3011' to '0.3000' on row '327'"
    ]
