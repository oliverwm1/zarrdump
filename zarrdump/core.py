import click
import fsspec
import xarray as xr


@click.command()
@click.argument("url")
def dump(url: str):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        print(f"zarrdump: No file or directory at {url}")
    else:
        m = fs.get_mapper(url)
        ds = _open_mapper(m)
        print(ds)


def _open_mapper(m: fsspec.FSMap) -> xr.Dataset:
    try:
        ds = xr.open_zarr(m, consolidated=True)
    except KeyError:
        ds = xr.open_zarr(m)
    return ds