from typing import Tuple, Union

import click
import fsspec
import xarray as xr
import zarr

ZARR_MAJOR_VERSION = zarr.__version__.split(".")[0]


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
@click.option("-m", "--max-rows", default=999, help="Maximum number of rows to display")
@click.option("-i", "--info", is_flag=True, help="Use ncdump style")
def dump(url: str, variable: str, max_rows: int, info: bool):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")

    object_, object_is_xarray = _open_with_xarray_or_zarr(url)

    if variable is not None:
        if info:
            raise click.ClickException("Cannot use both '-v' and '-i' options")
        object_ = object_[variable]

    if not object_is_xarray:
        object_ = object_.info

    if object_is_xarray and info:
        object_.info()
    else:
        with xr.set_options(display_max_rows=max_rows):
            print(object_)


def _open_with_xarray_or_zarr(
    url: str,
) -> Tuple[Union[xr.Dataset, zarr.Group, zarr.Array], bool]:
    if ZARR_MAJOR_VERSION >= "3":
        # TODO: remove ValueError here once a version of xarray is released
        # with https://github.com/pydata/xarray/pull/10025 merged
        exceptions = (KeyError, ValueError)
    else:
        exceptions = (KeyError, TypeError)

    try:
        result = xr.open_zarr(url)
        is_xarray_dataset = True
    except exceptions:
        # xarray cannot open dataset, fall back to using zarr directly
        result = zarr.open(url)
        is_xarray_dataset = False

    return result, is_xarray_dataset
