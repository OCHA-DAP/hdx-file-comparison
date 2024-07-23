#!/usr/bin/env python
# encoding: utf-8

import os
import time
from hdx_file_comparison.utilities import difflib_compare


def test_difflib_compare_small():
    filepath_1 = os.path.join(
        os.path.dirname(__file__), "fixtures", "2024-07-21-wfp_food_prices_afg_qc.csv"
    )
    # Manually removed lines from start and end, and mutated a value
    filepath_2 = os.path.join(
        os.path.dirname(__file__), "fixtures", "2024-07-21-wfp_food_prices_afg_qc_changed.csv"
    )

    t0 = time.time()
    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    for row in diff:
        print(row, flush=True)

    assert False


def test_difflib_compare_big():
    filepath_1 = os.path.join(
        os.path.dirname(__file__), "fixtures", "2024-07-21-wfp_food_prices_afg.csv"
    )
    # Manually removed lines from start and end, and mutated a value
    filepath_2 = os.path.join(
        os.path.dirname(__file__), "fixtures", "2024-07-21-wfp_food_prices_afg_changed.csv"
    )

    t0 = time.time()
    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")
    print(f"Diff took {time.time()-t0:0.3f} seconds", flush=True)

    for row in diff:
        if row.startswith("?"):
            print(f"'{row}'", flush=True)

    assert False
