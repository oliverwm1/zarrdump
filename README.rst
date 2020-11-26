Describe zarr stores from the command line. Any path to a "filesystem" backed by `fsspec <https://github.com/intake/filesystem_spec>`_ is valid.

Usage
-----

::

    $ zarrdump /local/dataset.zarr
    <xarray.Dataset>
    Dimensions:  (lat: 73, lon: 144, plev: 64, time: 32)
    Coordinates:
    * lat      (lat) float64 -90.0 -87.5 -85.0 -82.5 -80.0 ... 82.5 85.0 87.5 90.0
    * lon      (lon) float64 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    * plev     (plev) float32 0.321235 1.010185 1.7987399 ... 991.65173 997.3356
    * time     (time) object 2016-12-01 00:00:00 ... 2017-01-01 00:00:00
    Data variables:
        ps       (time, lat, lon) float32 dask.array<chunksize=(4, 73, 144), meta=np.ndarray>
        ta       (time, plev, lat, lon) float32 dask.array<chunksize=(4, 64, 73, 144), meta=np.ndarray>
        ua       (time, plev, lat, lon) float32 dask.array<chunksize=(4, 64, 73, 144), meta=np.ndarray>
        va       (time, plev, lat, lon) float32 dask.array<chunksize=(4, 64, 73, 144), meta=np.ndarray>


    $ zarrdump -v ta gs://bucket/dataset.zarr
    <xarray.DataArray 'ta' (time: 32, plev: 64, lat: 73, lon: 144)>
    dask.array<zarr, shape=(32, 64, 73, 144), dtype=float32, chunksize=(4, 64, 73, 144), chunktype=numpy.ndarray>
    Coordinates:
    * lat      (lat) float64 -90.0 -87.5 -85.0 -82.5 -80.0 ... 82.5 85.0 87.5 90.0
    * lon      (lon) float64 0.0 2.5 5.0 7.5 10.0 ... 350.0 352.5 355.0 357.5
    * plev     (plev) float32 0.321235 1.010185 1.7987399 ... 991.65173 997.3356
    * time     (time) object 2016-12-01 00:00:00 ... 2017-01-01 00:00:00
    Attributes:
        longname:  temperature
        units:     K

Installation
------------

::

    $ pip install zarrdump