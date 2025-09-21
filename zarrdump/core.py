from typing import Optional, Union

import click
import fsspec
import xarray as xr
import zarr

ZARR_MAJOR_VERSION = zarr.__version__.split(".")[0]


# From https://stackoverflow.com/questions/51164033/python-click-multiple-key-value-pair-arguments
def _attributes_to_dict(
    ctx: click.Context, attribute: click.Option, attributes: Optional[tuple[str, ...]]
) -> Optional[dict[str, str]]:
    """Click callback that converts attributes specified in the form `key=value` to a
    dictionary"""
    if attributes is None or len(attributes) == 0:
        return None
    else:
        result = {}
        for arg in attributes:
            k, v = arg.split("=")
            if k in result:
                raise click.BadParameter(f"Attribute {k!r} is specified twice")
            result[k] = v

    return result


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
@click.option("-m", "--max-rows", default=999, help="Maximum number of rows to display")
@click.option("-i", "--info", is_flag=True, help="Use ncdump style")
@click.option(
    "--storage-option",
    help="Key/value pair separated by '=', to be passed to the storage_options "
    "argument of fsspec. It can be used multiple times to pass multiple "
    "arguments. For example: --storage-option profile=contabo "
    "--storage-option endpoint=https://eu2.contabostorage.com",
    multiple=True,
    callback=_attributes_to_dict,
    default=None,
)
def dump(
    url: str,
    variable: str,
    max_rows: int,
    info: bool,
    storage_option: Optional[dict[str, str]],
):
    fs, _, _ = fsspec.get_fs_token_paths(url, storage_options=storage_option)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")

    object_, object_is_xarray = _open_with_xarray_or_zarr(url, storage_option)

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
    url: str, storage_option: Optional[dict[str, str]] = None
) -> tuple[Union[xr.Dataset, zarr.Group, zarr.Array], bool]:
    if ZARR_MAJOR_VERSION >= "3":
        # TODO: remove ValueError here once a version of xarray is released
        # with https://github.com/pydata/xarray/pull/10025 merged
        exceptions = (KeyError, ValueError)
    else:
        exceptions = (KeyError, TypeError)

    try:
        result = xr.open_zarr(url, storage_options=storage_option)
        is_xarray_dataset = True
    except exceptions:
        # xarray cannot open dataset, fall back to using zarr directly
        result = zarr.open(url, storage_options=storage_option)
        is_xarray_dataset = False

    return result, is_xarray_dataset
