# ODSE 2022 Deep Learning utility package

## Install

Install dependencies:

`pip install rasterio requests geopandas`

Install `odse_dl`:

`pip install "git+https://gitlab.com/geoharmonizer_inea/odse-workshop-2022.git#subdirectory=python_training/packages/odse_dl"`

## Usage

### Data utilities

#### Raster datasets

`In [1]: from odse_dl import data`

The `data` submodule includes helpers for loading the target data and downloading inputs aligned to the target tiles.

`target_files` contains a dict of target files for each tile.

```
In [2]: data.target_files
Out[2]:
{'t1': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t1.tif'),
 't2': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t2.tif'),
 't3': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t3.tif'),
 't4': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t4.tif'),
 't5': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t5.tif'),
 't7': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t7.tif'),
 't8': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t8.tif'),
 't9': PosixPath('/home/luka/miniconda3/envs/gis39/lib/python3.9/site-packages/odse_dl-0.1.0-py3.9.egg/odse_dl/dist_data/target_t9.tif')}
```

`get_tile_geometries()` returns a `geopandas.GeoDataFrame` of tile names and bounding boxes.

```
In [3]: data.get_tile_geometries()
Out[3]:
  name                                           geometry
0   t1  POLYGON ((4634730.000 2993230.000, 4634730.000...
1   t2  POLYGON ((4634730.000 3000730.000, 4634730.000...
2   t3  POLYGON ((4634730.000 3008230.000, 4634730.000...
3   t4  POLYGON ((4642230.000 2993230.000, 4642230.000...
4   t5  POLYGON ((4642230.000 3000730.000, 4642230.000...
5   t6  POLYGON ((4642230.000 3008230.000, 4642230.000...
6   t7  POLYGON ((4649730.000 2993230.000, 4649730.000...
7   t8  POLYGON ((4649730.000 3000730.000, 4649730.000...
8   t9  POLYGON ((4649730.000 3008230.000, 4649730.000...
```

`input_data_to_tiles()` arranges input rasters into tiles and returns a dict containing a list of input files for each tile.

```
In [4]: files = data.input_data_to_tiles(
   ...:     ['input_raster.tif'], # iterable of input rasters
   ...:     out_dir='./',         # defaults to working directory
   ...:     n_threads=8,          # defaults to logical cpu count
   ...: )
[22:16:05] clipped datasets to tile 1 of 9
[22:16:05] clipped datasets to tile 2 of 9
[22:16:05] clipped datasets to tile 3 of 9
[22:16:05] clipped datasets to tile 4 of 9
[22:16:05] clipped datasets to tile 5 of 9
[22:16:05] clipped datasets to tile 6 of 9
[22:16:05] clipped datasets to tile 7 of 9
[22:16:05] clipped datasets to tile 8 of 9
[22:16:05] clipped datasets to tile 9 of 9

In [5]: files
Out[5]:
{'t1': [PosixPath('input_raster_t1.tif')],
 't2': [PosixPath('input_raster_t2.tif')],
 't3': [PosixPath('input_raster_t3.tif')],
 't4': [PosixPath('input_raster_t4.tif')],
 't5': [PosixPath('input_raster_t5.tif')],
 't6': [PosixPath('input_raster_t6.tif')],
 't7': [PosixPath('input_raster_t7.tif')],
 't8': [PosixPath('input_raster_t8.tif')],
 't9': [PosixPath('input_raster_t9.tif')]}
```

`get_sentinel_tiles()` is a convenience function that calls `input_data_to_tiles` on all urls in `data.sentinel_urls` (which contains urls of Geo-harmonizer seasonal mosaics of P25, P50 and P75 of visible and infrared Sentinel 2 bands for 2018) to download the mosaic subsets (with identical keyword arguments as `input_data_to_tiles`).

```
In [6]: files = data.get_sentinel_tiles()
[22:21:57] downloaded datasets for tile 1 of 9
[22:22:22] downloaded datasets for tile 2 of 9
...

In [7]: files
Out[8]:
{'t1': [PosixPath('input_data/lcv_blue_sentinel.s2l2a_p25_30m_0..0cm_2017.12.02..2018.03.20_eumap_epsg3035_v1.0_t1.tif'),
  PosixPath('input_data/lcv_blue_sentinel.s2l2a_p25_30m_0..0cm_2018.03.21..2018.06.24_eumap_epsg3035_v1.0_t1.tif'),
  PosixPath('input_data/lcv_blue_sentinel.s2l2a_p25_30m_0..0cm_2018.06.25..2018.09.12_eumap_epsg3035_v1.0_t1.tif'),
  PosixPath('input_data/lcv_blue_sentinel.s2l2a_p25_30m_0..0cm_2018.09.13..2018.12.01_eumap_epsg3035_v1.0_t1.tif'),
...
```

If you'd like to cherry pick the sentinel layers to download, you can filter `data.sentinel_urls` and call `input_data_to_tiles()` on the output.

#### Legend

The `legend` module provides semantics for all three legend levels...

```
In [1]: from odse_dl import legend

In [2]: legend.level1
Out[2]: {0: 'Non-artificial', 1: 'Artificial'}

In [3]: legend.level2
Out[3]: {0: 'Water', 1: 'Artificial', 2: 'Vegetation'}

In [4]: legend.level3
Out[4]:
{0: 'Water',
 1: 'Urban fabric',
 2: 'Non-housing builtup',
 3: 'Urban green areas',
 4: 'Infrastructure',
 5: 'Unsorted artificial',
 6: 'Agriculture',
 7: 'Forest',
 8: 'Non-forest vegetation'}
```

...reverse dicts for each level...

```
In [5]: legend.level1_reverse
Out[5]: {'Non-artificial': 0, 'Artificial': 1}
```

...as well as aggregators to lower legend levels.

```
In [6]: legend.agg3to2
Out[6]: {0: 0, 1: 1, 2: 1, 4: 1, 5: 1, 3: 2, 6: 2, 7: 2, 8: 2}

In [7]: legend.agg2to1
Out[7]: {0: 0, 2: 0, 1: 1}

In [8]: legend.agg3to1
Out[8]: {0: 0, 3: 0, 6: 0, 7: 0, 8: 0, 1: 1, 2: 1, 4: 1, 5: 1}
```

Each legend level and aggregator has a `_transform` counterpart which can be indexed to transform data...

```
In [9]: import numpy as np

In [10]: data = np.arange(9).reshape(3, 3)

In [11]: data
Out[11]:
array([[0, 1, 2],
       [3, 4, 5],
       [6, 7, 8]])

In [12]: legend.level3_transform[data]
Out[12]:
array([['Water', 'Urban fabric', 'Non-housing builtup'],
       ['Urban green areas', 'Infrastructure', 'Unsorted artificial'],
       ['Agriculture', 'Forest', 'Non-forest vegetation']], dtype=object)

In [13]: legend.agg3to2_transform[data]
Out[13]:
array([[0, 1, 1],
       [2, 1, 1],
       [2, 2, 2]], dtype=uint8)
```

...or you could use the `transform()` function to transform data with an arbitrary dict.

```
In [15]: legend.transform(legend.agg3to1, data)
Out[15]:
array([[0, 1, 1],
       [0, 1, 1],
       [0, 0, 0]], dtype=uint8)
```

### DL contest client

The `contest` module provides means to register and submit results to the contest.

Calling `register()` with a name you wish to use for the contest takes care of registration and saves your credentials to the current working directory.

```
In [1]: from odse_dl import contest

In [2]: token = contest.register('Contestant')
Thanks for participating, Contestant!
Credentials saved to /home/contestant/odse2022_contest_credentials.json
Your token is jjj05ZENM8ldQT-8-Vkdmx7aVeXpHLV9nGzc3tOnokO_ksFz8ME8chm3y2MPMh1M0M7M3wI8LXFDFso-Y8UKRw
```

You can `submit()` your results by passing either a path to a GeoTiff of a NumPy array...

```
In [3]: contest.submit('results.tif')
              precision    recall  f1-score   support

           0       0.01      0.01      0.01      2604
           1       0.26      0.37      0.30     17971
           2       0.13      0.19      0.16      9457
           3       0.09      0.16      0.12      7463
           4       0.03      0.08      0.05      2349
           5       0.00      0.00      0.00        90
           6       0.03      0.00      0.01     16453
           7       0.00      0.00      0.00      5362
           8       0.00      0.00      0.00       751

    accuracy                           0.16     62500
   macro avg       0.06      0.09      0.07     62500
weighted avg       0.11      0.16      0.13     62500
```

...and view the current `scoreboard()` (this does not require registration).

```
In [4]: contest.scoreboard()
  #  name           score
---  ----------  --------
  1  Contestant  0.128763
```

The contest client can also be used from your preferred shell, e.g.:

```
python -m odse_dl.contest register Contestant
python -m odse_dl.contest submit results.tif
python -m odse_dl.contest scoreboard
```

#### Rebuilding credentials

If you have lost your credentials file (`odse2022_contest_credentials.json`) but have not lost your API token, you can run `contest.rebuild_credentials(token)` to retrieve your username and store the credentials in the file again.

#### Running from Colab

If you're running competition code from Google Colab the credentials file will be deleted when your runtime disconnects. To circumvent this, you can run `contest.drive.store_credentials()` to save the credentials to the root of your Google Drive, and then run `contest.drive.retrieve_credentials()` on each subsequent session. This will, howerer, require giving your Colab account permission to write to your drive. Otherwise, you can rebuild credentials using your token (see above).
