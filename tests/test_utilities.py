#!/usr/bin/env python
# encoding: utf-8

import os
import time
from hdx_file_comparison.utilities import (
    difflib_compare,
    process,
    compute_diff_metrics,
    difflib_column_changes,
)

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
    assert diff_metrics["n_lines_added"] == 1


def test_process():
    t0 = time.time()
    diff_metrics = process(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED)
    print(f"Process took {time.time()-t0:0.3f} seconds", flush=True)

    print(diff_metrics, flush=True)
    assert diff_metrics == {
        "n_lines_changed": 2.0,
        "n_lines_added": 4.0,
        "n_lines_removed": 0.0,
        "cell_changes": [
            {"row": 291, "column": "usdprice", "original_value": "0.3606", "new_value": "0.331"},
            {
                "row": 589,
                "column": "date",
                "original_value": "2024-05-15",
                "new_value": "2024-06-15",
            },
        ],
    }


def test_difflib_column_changes():
    t0 = time.time()
    diff_columns = difflib_column_changes(SMALL_FILE_ORIGINAL, SMALL_FILE_CHANGED)
    print(f"Process took {time.time()-t0:0.3f} seconds", flush=True)

    print(diff_columns, flush=True)

    assert diff_columns == {
        "date": [
            (291, "+ 2024-06-15"),
            (292, "+ 2024-07-15"),
            (585, "+ 2024-06-15"),
            (586, "+ 2024-07-15"),
            (650, "- 2005-04-15"),
            (651, "- 2005-05-15"),
            (652, "- 2005-06-15"),
            (653, "- 2005-07-15"),
        ],
        "code": None,
        "usdprice": [
            (290, "- 0.3606"),
            (291, "+ 0.331"),
            (292, "+ 0.2365"),
            (293, "+ 0.2681"),
            (585, "+ 0.6962"),
            (587, "+ 0.7055"),
            (651, "- 0.3272"),
            (652, "- 0.2991"),
            (653, "- 0.3342"),
            (654, "- 0.3225"),
        ],
    }
