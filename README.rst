Describe zarr stores from the command line.

Usage
-----

::

    $ zarrdump /path/to/dataset.zarr
    <xarray.Dataset>
    Dimensions:  (x: 3, y: 6)
    Dimensions without coordinates: x, y
    Data variables:
        temperature        (x, y) float64 ...


Installation
------------

::

    $ pip install zarrdump