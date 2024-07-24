#!/usr/bin/env python
# encoding: utf-8

import os
import time
from hdx_file_comparison.utilities import difflib_compare, process, compute_diff_metrics

FIXTURES_DIRECTORY = os.path.join(os.path.dirname(__file__), "fixtures")
SMALL_FILE_ORIGINAL = os.path.join(FIXTURES_DIRECTORY, "2024-05-12-wfp_food_prices_afg_qc.csv")
SMALL_FILE_CHANGED = os.path.join(FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg_qc.csv")
BIG_FILE_ORIGINAL = os.path.join(FIXTURES_DIRECTORY, "2024-07-14-wfp_food_prices_afg.csv")
BIG_FILE_CHANGED = os.path.join(FIXTURES_DIRECTORY, "2024-07-21-wfp_food_prices_afg.csv")


def test_difflib_compare_small():
    t0 = time.time()
    diff = difflib_compare(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    diff_metrics = compute_diff_metrics(diff)
    print(diff_metrics, flush=True)
    for row in diff:
        print(row, flush=True)

    assert diff_metrics["n_lines_changed"] == 2
    assert diff_metrics["n_lines_removed"] == 0
    assert diff_metrics["n_lines_added"] == 4


def test_difflib_compare_big():
    t0 = time.time()
    diff = difflib_compare(BIG_FILE_ORIGINAL, BIG_FILE_CHANGED, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    diff_metrics = compute_diff_metrics(diff)
    print(diff_metrics, flush=True)
    # for row in diff:
    #     print(row, flush=True)

    assert diff_metrics["n_lines_changed"] == 473
    assert diff_metrics["n_lines_removed"] == 0
    assert diff_metrics["n_lines_added"] == 1.0


def test_process():
    t0 = time.time()
    cell_changes = process(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED)
    print(f"Process took {time.time()-t0:0.3f} seconds", flush=True)

    print(cell_changes, flush=True)
    assert cell_changes == [
        "Column 'usdprice' has been changed from '0.3606' to '0.331' on row '291'",
        "Column 'date' has been changed from '2024-05-15' to '2024-06-15' on row '589'",
    ]
