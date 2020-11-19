from typing import Union

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
    zarr_obj, consolidated = _open_zarr(m)

    if _zarr_object_is_xarray_dataset(zarr_obj):
        printme = xr.open_zarr(m, consolidated=consolidated)
        object_is_xarray = True
    else:
        printme = zarr_obj
        object_is_xarray = False

    if variable is not None:
        printme = printme[variable]

    if not object_is_xarray:
        printme = printme.info

    print(printme)


def _open_zarr(m: fsspec.FSMap) -> Union[zarr.hierarchy.Group, zarr.core.Array]:
    try:
        result = zarr.open_consolidated(m)
        consolidated=True
    except KeyError:
        # un-consolidated group, or array
        result = zarr.open(m)
        consolidated=False

    return result, consolidated


def _zarr_object_is_xarray_dataset(
    obj: Union[zarr.hierarchy.Group, zarr.core.Array]
    ) -> bool:
    try:
        array_keys = list(obj.keys())
    except AttributeError:
        is_xarray_dataset = False
    else:
        array = obj[array_keys[0]]
        required_xarray_attr = xr.backends.zarr.DIMENSION_KEY
        is_xarray_dataset = True if required_xarray_attr in array.attrs else False
    return is_xarray_dataset
