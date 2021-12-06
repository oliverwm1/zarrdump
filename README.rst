.. image:: https://img.shields.io/pypi/v/zarrdump.svg
   :target: https://pypi.org/project/zarrdump/

Describe `zarr <https://github.com/zarr-developers/zarr-python>`_ stores from the command line. A path to any filesystem implemented by `fsspec <https://github.com/intake/filesystem_spec>`_ is valid.

Installation
------------

::

    $ pip install zarrdump

Usage
-----

If zarr store can be opened by `xarray <https://github.com/pydata/xarray>`_, the xarray representation will be displayed:
::

    $ zarrdump gs://bucket/dataset.zarr
    <xarray.Dataset>
    Dimensions:  (lat: 73, lon: 144, time: 32)
    Coordinates:
    * lat      (lat) float64 -90.0 -87.5 -85.0 -82.5 -80.0 ... 82.5 85.0 87.5 90.0
    * lon      (lon) float64 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    * time     (time) object 2016-12-01 00:00:00 ... 2017-01-01 00:00:00
    Data variables:
        ps       (time, lat, lon) float32 dask.array<chunksize=(4, 73, 144), meta=np.ndarray>
        ts       (time, lat, lon) float32 dask.array<chunksize=(4, 73, 144), meta=np.ndarray>


Can show information for a particular variable/array:
::

    $ zarrdump -v ts gs://bucket/dataset.zarr
    <xarray.DataArray 'ts' (time: 32, lat: 73, lon: 144)>
    dask.array<zarr, shape=(32, 73, 144), dtype=float32, chunksize=(4, 73, 144), chunktype=numpy.ndarray>
    Coordinates:
    * lat      (lat) float64 -90.0 -87.5 -85.0 -82.5 -80.0 ... 82.5 85.0 87.5 90.0
    * lon      (lon) float64 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    * time     (time) object 2016-12-01 00:00:00 ... 2017-01-01 00:00:00
    Attributes:
        longname:  surface temperature
        units:     K

Diagnostic information will also be printed for zarr arrays or zarr groups which do not represent xarray datasets:
::

    $ zarrdump group.zarr
    Name        : /
    Type        : zarr.hierarchy.Group
    Read-only   : False
    Store type  : fsspec.mapping.FSMap
    No. members : 2
    No. arrays  : 2
    No. groups  : 0
    Arrays      : bar, foo
