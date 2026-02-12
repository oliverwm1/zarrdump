zarrdump
========

.. image:: https://img.shields.io/pypi/v/zarrdump.svg
   :target: https://pypi.org/project/zarrdump/
.. image:: https://img.shields.io/pypi/pyversions/zarrdump.svg
   :target: https://pypi.org/project/zarrdump/
.. image:: https://github.com/oliverwm1/zarrdump/actions/workflows/pytest.yaml/badge.svg
   :target: https://github.com/oliverwm1/zarrdump/actions/workflows/pytest.yaml
.. image:: https://img.shields.io/pypi/l/zarrdump.svg
   :target: https://github.com/oliverwm1/zarrdump/blob/main/LICENSE


Describe `zarr <https://github.com/zarr-developers/zarr-python>`_ stores from the command line.
A path to any filesystem implemented by `fsspec <https://github.com/fsspec/filesystem_spec>`_ is valid.
Inspired by `ncdump <https://docs.unidata.ucar.edu/nug/current/netcdf_utilities_guide.html#ncdump_guide>`_.

Installation
------------

::

    $ pip install zarrdump

CLI Reference
-------------

::

    $ zarrdump --help
    Usage: zarrdump [OPTIONS] URL

    Options:
      -v, --variable TEXT     Dump variable's info
      -m, --max-rows INTEGER  Maximum number of rows to display
      -i, --info              Use ncdump style
      --storage-option TEXT   Key/value pair separated by '=', to be passed to the
                              storage_options argument of fsspec. It can be used
                              multiple times to pass multiple arguments. For
                              example: --storage-option profile=contabo --storage-
                              option endpoint=https://eu2.contabostorage.com
      --obstore               Use obstore backend instead of fsspec
      --help                  Show this message and exit.

Usage
-----

If zarr store can be opened by `xarray <https://github.com/pydata/xarray>`_, the xarray representation will be displayed:
::

    $ zarrdump gs://bucket/dataset.zarr
    <xarray.Dataset> Size: 3MB
    Dimensions:  (time: 32, lat: 73, lon: 144)
    Coordinates:
      * time     (time) int64 256B 0 1 2 3 4 5 6 7 8 ... 23 24 25 26 27 28 29 30 31
      * lat      (lat) float64 584B -90.0 -87.5 -85.0 -82.5 ... 82.5 85.0 87.5 90.0
      * lon      (lon) float64 1kB 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    Data variables:
        ps       (time, lat, lon) float32 1MB dask.array<chunksize=(16, 37, 144), meta=np.ndarray>
        ts       (time, lat, lon) float32 1MB dask.array<chunksize=(16, 37, 144), meta=np.ndarray>


Can show information for a particular variable/array:
::

    $ zarrdump -v ts gs://bucket/dataset.zarr
    <xarray.DataArray 'ts' (time: 32, lat: 73, lon: 144)> Size: 1MB
    dask.array<open_dataset-ts, shape=(32, 73, 144), dtype=float32, chunksize=(16, 37, 144), chunktype=numpy.ndarray>
    Coordinates:
      * time     (time) int64 256B 0 1 2 3 4 5 6 7 8 ... 23 24 25 26 27 28 29 30 31
      * lat      (lat) float64 584B -90.0 -87.5 -85.0 -82.5 ... 82.5 85.0 87.5 90.0
      * lon      (lon) float64 1kB 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    Attributes:
        longname:  surface temperature
        units:     K

Diagnostic information will also be printed for zarr arrays or zarr groups which do not represent xarray datasets:
::

    $ zarrdump group.zarr
    Name        :
    Type        : Group
    Zarr format : 3
    Read-only   : False
    Store type  : LocalStore
