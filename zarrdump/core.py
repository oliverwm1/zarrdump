from typing import Tuple, Union

import click
import fsspec
import xarray as xr
import zarr


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
def dump(url: str, variable: str):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")

    m = fs.get_mapper(url)
    consolidated = _metadata_is_consolidated(m)
    printme, object_is_xarray = _open_with_xarray_or_zarr(m, consolidated)

    if variable is not None:
        printme = printme[variable]

    if not object_is_xarray:
        printme = printme.info

    print(printme)


def _metadata_is_consolidated(m: fsspec.FSMap) -> bool:
    try:
        zarr.open_consolidated(m)
        consolidated = True
    except KeyError:
        # group with un-consolidated metadata, or array
        consolidated = False
    return consolidated


def _open_with_xarray_or_zarr(
    m: fsspec.FSMap, consolidated: bool
) -> Tuple[Union[xr.Dataset, zarr.hierarchy.Group, zarr.core.Array], bool]:
    try:
        result = xr.open_zarr(m, consolidated=consolidated)
        is_xarray_dataset = True
    except KeyError:
        # xarray requires _ARRAY_DIMENSIONS attribute, assuming missing if KeyError
        result = zarr.open_consolidated(m) if consolidated else zarr.open(m)
        is_xarray_dataset = False
    return result, is_xarray_dataset
