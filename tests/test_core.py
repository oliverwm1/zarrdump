import zarrdump
from zarrdump.core import _open_mapper, dump

from click.testing import CliRunner
import fsspec
import pytest
import xarray as xr


def test_version():
    assert zarrdump.__version__ == '0.1.1'


@pytest.mark.parametrize("consolidated", [True, False])
def test__open_mapper(tmpdir, consolidated):
    ds = xr.Dataset({"var1": xr.DataArray(range(3))})
    path = str(tmpdir.join("test.zarr"))
    ds.to_zarr(path, consolidated=consolidated)
    ds2 = _open_mapper(fsspec.get_mapper(path))
    xr.testing.assert_identical(ds, ds2)


def test_dump_non_existent_url():
    runner = CliRunner()
    result = runner.invoke(dump, ["non/existent/path"])
    assert result.exit_code == 0
    assert result.output == "zarrdump: No file or directory at non/existent/path\n"
