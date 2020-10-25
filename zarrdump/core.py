import click
import fsspec
import xarray as xr


@click.command()
@click.argument("url")
@click.option("-v", "--variable", type=str, help="Dump variable's info")
def dump(url: str, variable: str):
    fs, _, _ = fsspec.get_fs_token_paths(url)
    if not fs.exists(url):
        raise click.ClickException(f"No file or directory at {url}")
    m = fs.get_mapper(url)
    printme = _open_mapper(m)
    if variable is not None:
        printme = printme[variable]
    print(printme)


def _open_mapper(m: fsspec.FSMap) -> xr.Dataset:
    try:
        ds = xr.open_zarr(m, consolidated=True)
    except KeyError:
        ds = xr.open_zarr(m)
    return ds