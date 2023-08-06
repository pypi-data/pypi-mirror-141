def map(arr, fn):
    return [fn(v, i, arr) for i, v in enumerate(arr)]
