#!/usr/bin/env python
# encoding: utf-8

import datetime
import os
import click
from hdx_file_comparison.utilities import (
    fetch_data_from_hapi,
    difflib_compare,
    compute_diff_metrics,
)
from typing import Optional

LIMIT = 1000


@click.group()
@click.version_option()
def hdx_compare() -> None:
    """Tools for comparing files from HAPI and HDX"""


@hdx_compare.command(name="download")
@click.option(
    "--theme",
    is_flag=False,
    default="metadata/admin1",
    help="target theme for download",
)
@click.option("--download_directory", is_flag=False, default=None, help="target_directory")
@click.option("--hapi_site", is_flag=False, default="hapi", help="target_directory")
def download(theme: str = "", download_directory: Optional[str] = None, hapi_site: str = "hapi"):
    if download_directory is None:
        download_directory = os.path.join(os.path.dirname(__file__), "output")
    email_address = "ian.hopkinson%40humdata.org"
    app_name = "hdx_file_comparison"

    app_identifier_url = (
        f"https://{hapi_site}.humdata.org/api/v1/"
        f"encode_app_identifier?application={app_name}&email={email_address}"
    )
    app_identifier_response = fetch_data_from_hapi(app_identifier_url)

    app_identifier = app_identifier_response["encoded_app_identifier"]

    print(app_identifier_response, flush=True)

    query_url = (
        f"https://{hapi_site}.humdata.org/api/v1/{theme}?"
        f"output_format=csv"
        f"&app_identifier={app_identifier}"
    )

    results = fetch_data_from_hapi(query_url, LIMIT)

    date_ = datetime.datetime.now().isoformat()[0:10]
    output_filename = f"{date_}-{theme.replace('/','_')}-{hapi_site}.csv"
    output_file_path = os.path.join(download_directory, output_filename)
    with open(output_file_path, "w") as output_file:
        for line in results:
            output_file.write(f"{line.decode('utf-8')}\n")


@hdx_compare.command(name="compare")
@click.option(
    "--theme",
    is_flag=False,
    default="metadata/admin1",
    help="target theme for download",
)
@click.option("--download_directory", is_flag=False, default="output", help="target_directory")
@click.option(
    "--file_1",
    is_flag=False,
    default="2024-08-06-metadata_admin1-hapi.csv",
    help="target_directory",
)
@click.option(
    "--file_2",
    is_flag=False,
    default="2024-08-06-metadata_admin1-hapi-temporary.csv",
    help="target_directory",
)
def compare(
    theme: str = "",
    download_directory: Optional[str] = None,
    file_1: str = "hapi",
    file_2: str = "hapi",
):
    filepath_1 = os.path.join(download_directory, file_1)
    filepath_2 = os.path.join(download_directory, file_2)

    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")

    # Process diff
    diff_metrics = compute_diff_metrics(diff)

    print(diff_metrics, flush=True)
