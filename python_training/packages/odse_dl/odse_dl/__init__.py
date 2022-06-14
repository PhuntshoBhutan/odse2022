try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

__version__ = '0.1.2'

from . import dist_data

def _get_resource_path(rel_path):
    with pkg_resources.path(dist_data, rel_path) as path:
        return path
