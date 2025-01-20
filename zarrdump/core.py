from typing import Tuple, Union

import click
import fsspec
import xarray as xr
import zarr


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
@click.option("-m", "--max-rows", default=999, help="Maximum number of rows to display")
@click.option("-i", "--info", is_flag=True, help="Use ncdump style")
def dump(url: str, variable: str, max_rows: int, info: bool):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")

    consolidated = _metadata_is_consolidated(url)
    object_, object_is_xarray = _open_with_xarray_or_zarr(url, consolidated)

    if variable is not None:
        if info:
            raise click.ClickException("Cannot use both '-v' and '-i' options")
        object_ = object_[variable]

    if not object_is_xarray:
        object_ = object_.info

    if object_is_xarray and info:
        object_.info()
    else:
        try:
            with xr.set_options(display_max_rows=max_rows):
                print(object_)
        except ValueError:
            # xarray<v0.18.0 does not have display_max_rows option
            print(object_)


def _metadata_is_consolidated(url: str) -> bool:
    try:
        zarr.open_consolidated(url)
        consolidated = True
    except (KeyError, ValueError):  # KeyError for zarr v2, ValueError for zarr v3
        # group with un-consolidated metadata, or array
        consolidated = False
    return consolidated


def _open_with_xarray_or_zarr(
    url: str, consolidated: bool
) -> Tuple[Union[xr.Dataset, zarr.Group, zarr.Array], bool]:
    try:
        result = xr.open_zarr(url, consolidated=consolidated)
        is_xarray_dataset = True
    except (KeyError, TypeError, ValueError):
        # xarray requires _ARRAY_DIMENSIONS attribute, assuming missing if KeyError
        result = zarr.open_consolidated(url) if consolidated else zarr.open(url)
        is_xarray_dataset = False
    return result, is_xarray_dataset
