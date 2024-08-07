#!/usr/bin/env python
# encoding: utf-8

import datetime
import os
import time

from typing import Optional

import click

from hdx_file_comparison.utilities import (
    fetch_data_from_hapi,
    difflib_compare,
    compute_diff_metrics,
)


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
@click.option(
    "--download_directory", is_flag=False, default=None, help="target directory for download"
)
@click.option(
    "--hapi_site",
    is_flag=False,
    default=None,
    help="HDX HAPI endpoint prefix, .humdata.org/api/v1/ is appended",
)
def download(theme: str = "", download_directory: Optional[str] = None, hapi_site: str = "hapi"):
    """Download HDX HAPI responses as CSV files"""
    download_file(theme, download_directory, hapi_site)


@hdx_compare.command(name="compare")
@click.option(
    "--theme",
    is_flag=False,
    default="metadata/admin1",
    help="target theme for download",
)
@click.option(
    "--download_directory",
    is_flag=False,
    default="output",
    help="Directory where files to compare are stored",
)
@click.option(
    "--file_1",
    is_flag=False,
    default="2024-08-06-metadata_admin1-hapi.csv",
    help="Filename for first file in comparison",
)
@click.option(
    "--file_2",
    is_flag=False,
    default="2024-08-06-metadata_admin1-hapi-temporary.csv",
    help="Filename for first file in comparison",
)
def compare(
    theme: str = "",
    download_directory: Optional[str] = None,
    file_1: str = "hapi",
    file_2: str = "hapi",
):
    """Compare files"""
    filepath_1 = os.path.join(download_directory, file_1)
    filepath_2 = os.path.join(download_directory, file_2)

    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")

    # Process diff
    diff_metrics = compute_diff_metrics(diff)

    print(diff_metrics, flush=True)


@hdx_compare.command(name="process")
@click.option(
    "--theme",
    is_flag=False,
    default="metadata/admin1",
    help="target theme for download",
)
@click.option("--download_directory", is_flag=False, default="output", help="target_directory")
def process(
    theme: str = "metadata/admin1",
    download_directory: Optional[str] = None,
):
    """Download and compare files from the hapi and hapi-temporary endpoints"""
    print_banner("process")
    filepath_1 = download_file(theme, download_directory, "hapi")
    filepath_2 = download_file(theme, download_directory, "hapi-temporary")

    t0 = time.time()
    print(f"Analysis started at {datetime.datetime.now().isoformat()} ", flush=True)
    diff = difflib_compare(filepath_1, filepath_2, encoding="utf-8")

    # Process diff
    diff_metrics = compute_diff_metrics(diff)
    print("\nChanged line counts:", flush=True)
    elapsed_time = time.time() - t0

    n_changes = 0
    for key, value in diff_metrics.items():
        n_changes += value

    if n_changes != 0:
        for row in diff:
            print(row, flush=True)
        for key, value in diff_metrics.items():
            n_changes += value
            print(f"{key}:{value}", flush=True)
        click.secho(
            f"\nFiles for theme '{theme}' are different, {n_changes} changes seen",
            fg="red",
            color=True,
        )
    else:
        for key, value in diff_metrics.items():
            n_changes += value
            print(f"{key}:{value}", flush=True)
        click.secho(
            f"\nFiles for theme '{theme}' are identical",
            fg="green",
            color=True,
        )

    print(f"Analysis took {elapsed_time:0.2f} seconds", flush=True)


def download_file(theme, download_directory, hapi_site):
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

    query_url = (
        f"https://{hapi_site}.humdata.org/api/v1/{theme}?"
        f"output_format=csv"
        f"&app_identifier={app_identifier}"
    )

    date_ = datetime.datetime.now().isoformat()[0:10]
    output_filename = f"{date_}-{theme.replace('/','_')}-{hapi_site}.csv"
    output_file_path = os.path.join(download_directory, output_filename)

    print(f"\nFetching data from: {query_url}", flush=True)
    print(f"Saving to: {output_file_path}", flush=True)

    results = fetch_data_from_hapi(query_url, LIMIT)

    print(f"Downloaded {len(results)} rows", flush=True)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(f"{line}\n")

    return output_file_path


def print_banner(action: str):
    """Simple function to output a banner to console, uses click's secho command but not colour
    because the underlying colorama does not output correctly to git-bash terminals.

    Arguments:
        action {str} -- _description_
    """
    title = f"HDX File Comparison - {action}"
    timestamp = f"Invoked at: {datetime.datetime.now().isoformat()}"
    width = max(len(title), len(timestamp))
    click.secho((width + 4) * "*", bold=True)
    click.secho(f"* {title:<{width}} *", bold=True)
    click.secho(f"* {timestamp:<{width}} *", bold=True)
    click.secho((width + 4) * "*", bold=True)
