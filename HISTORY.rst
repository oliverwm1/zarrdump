v0.5.0 (2025-03--07)
-------------------

- add support for zarr-python>=3.0.0
- drop support for xarray<0.19.0
- defer to xarray/zarr for handling consolidated metadata


v0.4.2 (2025-01-20)
-------------------

- pin zarr-python dependency to below version 3
- specify python>=3.8 requirement in setup.py

v0.4.1 (2022-08-22)
-------------------

- ensure can open and dump zarr group when xarray v2022.06.0 installed

v0.4.0 (2022-08-13)
-------------------

- add -m/--max-rows option to allow setting the xarray display_max_rows option. Default is set to 999.

v0.3.0 (2021-12-05)
-------------------

- add -i/--info flag to allow printing with ncdump-style using xr.Dataset.info()

v0.2.2 (2021-03-28)
-------------------

- change implementation for checking whether object is an xarray dataset
- apply black formatting

v0.2.1 (2020-11-26)
-------------------

- remove gcsfs from requirements
- improve README and pypi page description

v0.2.0 (2020-11-18)
-------------------

- allowing dumping info for zarr arrays or zarr groups that don't represent xarray datasets
- add -v option to print info for specific variable in dataset or group

v0.1.1 (2020-10-04)
-------------------

- bug fix

v0.1.0 (2020-09-22)
-------------------

- initial implementation