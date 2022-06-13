from pathlib import Path
import geopandas as gp
import rasterio as rio
from typing import List, Iterable, Union, Callable
import multiprocessing as mp
from multiprocessing.pool import ThreadPool

from . import misc, pkg_resources, _get_resource_path

CRS = 'EPSG:3035'
OUT_DIR_DEFAULT = Path('input_data')

with open(_get_resource_path('sentinel_urls.txt')) as src:
    sentinel_urls = [*map(str.strip, src)]

target_files = {
    path.stem[-2:]: path
    for path in map(
        lambda i: _get_resource_path(f'target_t{i}.tif'),
        # (1, 2, 3, 4, 5, 7, 8, 9),
        (1, 3, 4),
    )
}

def get_tile_geometries() -> gp.GeoDataFrame:
    return gp.read_file(_get_resource_path('tiles.geojson'))

def _get_raster_tile(
    row: gp.GeoSeries,
    out_dir: Union[str, Path]=OUT_DIR_DEFAULT,
) -> Callable:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def wrapped(source_path: Union[str, Path]) -> Path:
        source_path = Path(source_path)
        out_path = out_dir / f'{source_path.stem}_{row["name"]}.tif'

        with rio.open(source_path) as src:
            with rio.vrt.WarpedVRT(src, crs=CRS) as vrt:
                window = rio.windows.from_bounds(
                    *row.geometry.bounds,
                    transform=vrt.transform,
                )
                with rio.open(
                    out_path, 'w',
                    **{
                        **vrt.profile,
                        'driver': 'GTiff',
                        'transform': vrt.window_transform(window),
                        'tiled': True,
                        'blockxsize': 64,
                        'blockysize': 64,
                        'compress': 'deflate',
                        'width': window.width,
                        'height': window.height,
                    }
                ) as dst:
                    dst.write(vrt.read(window=window))

        return out_path
    return wrapped

def input_data_to_tiles(
    source_paths: Iterable[Union[str, Path]],
    out_dir: Union[str, Path]=OUT_DIR_DEFAULT,
    n_threads: int=mp.cpu_count(),
) -> dict:
    source_paths = [*source_paths]
    tiles = get_tile_geometries()

    out_paths = {}
    for i, row in tiles.iterrows():
        with ThreadPool(n_threads) as pool:
            out_paths[row['name']] = pool.map(
                _get_raster_tile(row, out_dir=out_dir),
                source_paths,
            )
        misc.ttprint(f'clipped datasets to tile {i+1} of {tiles.shape[0]}')

    return out_paths

def get_sentinel_tiles(
    out_dir: Union[str, Path]=OUT_DIR_DEFAULT,
    n_threads: int=mp.cpu_count(),
) -> dict:
    return input_data_to_tiles(
        sentinel_urls,
        out_dir=out_dir,
        n_threads=n_threads,
    )
