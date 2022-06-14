import numpy as np
from functools import reduce
from operator import add

level1 = {
    0: 'Non-artificial',
    1: 'Artificial',
}

level2 = {
    0: 'Water',
    1: 'Artificial',
    2: 'Vegetation',
}

level3 = {
    0: 'Water',
    1: 'Urban fabric',
    2: 'Non-housing builtup',
    3: 'Urban green areas',
    4: 'Infrastructure',
    5: 'Unsorted artificial',
    6: 'Agriculture',
    7: 'Forest',
    8: 'Non-forest vegetation',
}

def _expand_aggregator(_agg):
    return {
        key: value
        for key_tuple, value in _agg.items()
        for key in key_tuple
    }

agg3to2 = _expand_aggregator({
    (0,): 0,
    (1, 2, 4, 5,): 1,
    (3, 6, 7, 8,): 2,
})

agg2to1 = _expand_aggregator({
    (0, 2,): 0,
    (1,): 1,
})

agg3to1 = _expand_aggregator({
    (0, 3, 6, 7, 8,): 0,
    (1, 2, 4, 5,): 1,
})

def _filter_globals(prefix):
    return [*filter(
        lambda k: k.startswith(prefix),
        globals().keys(),
    )]

globals()['_levels'] = _filter_globals('level')
globals()['_aggregators'] = _filter_globals('agg')

for l in _levels:
    globals()[f'{l}_reverse'] = {
        v: k
        for k, v in globals()[l].items()
    }

def _dict2transformer(dict_):
    dtype = np.uint8
    if isinstance([*dict_.items()][0][1], str):
        dtype = object
    transformer = np.empty(
        shape=max([*dict_.keys()])+1,
        dtype=dtype,
    )
    for key, val in dict_.items():
        transformer[key] = val
    return transformer

for key in _levels + _aggregators:
    globals()[f'{key}_transform'] = _dict2transformer(globals()[key])

def transform(key, data):
    return _dict2transformer(key)[data]
