from typing import Union

import click
import fsspec
import xarray as xr
import zarr as zarr_pkg


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
@click.option("-m", "--max-rows", default=999, help="Maximum number of rows to display")
@click.option("-i", "--info", is_flag=True, help="Use ncdump style")
@click.option(
    "-z",
    "--zarr",
    is_flag=True,
    help="Open the given URL using zarr-python instead of xarray.",
)
def dump(url: str, variable: str, max_rows: int, info: bool, zarr: bool):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")

    if info and zarr:
        raise click.ClickException("Cannot use both '-z' and '-i' options")

    if variable is not None and info:
        raise click.ClickException("Cannot use both '-v' and '-i' options")

    m = fs.get_mapper(url)
    consolidated = _metadata_is_consolidated(m)

    if zarr:
        object_ = _open_with_zarr(m, consolidated)
    else:
        object_ = _open_with_xarray(m, consolidated)

    if variable is not None:
        object_ = object_[variable]

    if zarr:
        print(object_.info)
    else:
        if info:
            object_.info()
        else:
            if xr.__version__ >= "0.18.0":
                with xr.set_options(display_max_rows=max_rows):
                    print(object_)
            else:
                # xarray<v0.18.0 does not have display_max_rows option
                print(object_)


def _metadata_is_consolidated(m: fsspec.FSMap) -> bool:
    try:
        zarr_pkg.open_consolidated(m)
        consolidated = True
    except KeyError:
        # group with un-consolidated metadata, or array
        consolidated = False
    return consolidated


def _open_with_xarray(m: fsspec.FSMap, consolidated: bool) -> xr.Dataset:
    return xr.open_zarr(m, consolidated=consolidated)


def _open_with_zarr(
    m: fsspec.FSMap, consolidated: bool
) -> Union[zarr_pkg.hierarchy.Group, zarr_pkg.core.Array]:
    return zarr_pkg.open_consolidated(m) if consolidated else zarr_pkg.open(m)
