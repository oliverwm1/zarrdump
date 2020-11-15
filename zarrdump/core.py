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
    printme, is_xarray_dataset = _open_mapper(m)
    if variable is not None:
        printme = printme[variable]
    if is_xarray_dataset:
        print(printme)
    else:
        print(printme.info)


def _open_mapper(m: fsspec.FSMap) -> Union[xr.Dataset, zarr.hierarchy.Group, zarr.core.Array]:
    try:
        result = zarr.open_consolidated(m)
        consolidated=True
    except KeyError:
        result = zarr.open(m)
        consolidated=False

    is_xarray_dataset = _zarr_object_is_xarray_dataset(result)

    if is_xarray_dataset:
        result = xr.open_zarr(m, consolidated=consolidated)
    
    return result, is_xarray_dataset


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
