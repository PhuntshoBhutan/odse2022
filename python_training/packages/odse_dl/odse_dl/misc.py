def ttprint(*args, **kwargs):
    from datetime import datetime
    import sys

    ts = f'[{datetime.now():%H:%M:%S}]'

    first, *rest = args
    if isinstance(first, str) and first.startswith('\n'):
        first = first[1:]
        ts = '\n' + ts

    args = (ts, first, *rest)

    print(*args, **kwargs, flush=True)
