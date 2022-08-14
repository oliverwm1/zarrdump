import zarrdump
from zarrdump.core import dump, _open_with_xarray_or_zarr

from click.testing import CliRunner
import fsspec
import pytest
import numpy as np
import xarray as xr
import zarr


def test_version():
    assert zarrdump.__version__ == "0.4.0"


@pytest.fixture()
def tmp_xarray_ds(tmpdir):
    def write_ds_to_zarr(consolidated=False, n_vars=1):
        ds = xr.Dataset(
            {f"var{i}": xr.DataArray(range(3)) for i in range(1, n_vars + 1)}
        )
        path = str(tmpdir.join("test.zarr"))
        ds.to_zarr(path, consolidated=consolidated)
        return ds, path

    return write_ds_to_zarr


@pytest.fixture()
def tmp_zarr_group(tmpdir):
    def write_group_to_zarr(consolidated=False):
        path = str(tmpdir.join("test.zarr"))
        z = zarr.open_group(path)
        arr = z.create_dataset("var1", shape=(3, 5))
        arr[:] = 1.0
        if consolidated:
            zarr.consolidate_metadata(path)
        return z, path

    return write_group_to_zarr


@pytest.mark.parametrize("consolidated", [True, False])
def test__open_with_xarray_or_zarr_on_zarr_group(tmp_zarr_group, consolidated):
    group, path = tmp_zarr_group(consolidated=consolidated)
    m = fsspec.get_mapper(path)
    opened_group, is_xarray_dataset = _open_with_xarray_or_zarr(m, consolidated)
    np.testing.assert_allclose(group["var1"], opened_group["var1"])
    assert not is_xarray_dataset


@pytest.mark.parametrize("consolidated", [True, False])
def test__open_with_xarray_or_zarr_on_xarray_ds(tmp_xarray_ds, consolidated):
    ds, path = tmp_xarray_ds(consolidated=consolidated)
    m = fsspec.get_mapper(path)
    opened_ds, is_xarray_dataset = _open_with_xarray_or_zarr(m, consolidated)
    np.testing.assert_allclose(ds["var1"], opened_ds["var1"])
    assert is_xarray_dataset


def test_dump_non_existent_url():
    runner = CliRunner()
    result = runner.invoke(dump, ["non/existent/path"])
    assert result.exit_code == 1
    assert result.output == "Error: No file or directory at non/existent/path\n"


@pytest.mark.parametrize("options", [[], ["-v", "var1"]])
def test_dump_executes_on_zarr_group(tmp_zarr_group, options):
    runner = CliRunner()
    _, path = tmp_zarr_group()
    result = runner.invoke(dump, [path] + options)
    assert result.exit_code == 0


@pytest.mark.parametrize("options", [[], ["-v", "var1"], ["--info"]])
def test_dump_executes_on_xarray_dataset(tmp_xarray_ds, options):
    runner = CliRunner()
    _, path = tmp_xarray_ds()
    result = runner.invoke(dump, [path] + options)
    assert result.exit_code == 0


def test_dump_disallowed_options(tmp_xarray_ds):
    runner = CliRunner()
    _, path = tmp_xarray_ds()
    result = runner.invoke(dump, [path, "-v", "var1", "-i"])
    assert result.exit_code == 1
    assert result.output == "Error: Cannot use both '-v' and '-i' options\n"


def test_dump_max_rows_default(tmp_xarray_ds):
    runner = CliRunner()
    _, path = tmp_xarray_ds(consolidated=True, n_vars=30)
    result = runner.invoke(dump, [path])
    assert len(result.output.split("\n")) > 30


def test_dump_max_rows_limited(tmp_xarray_ds):
    runner = CliRunner()
    _, path = tmp_xarray_ds(consolidated=True, n_vars=30)
    result = runner.invoke(dump, [path, "-m", 10])
    assert len(result.output.split("\n")) < 20  # give some buffer over 10
