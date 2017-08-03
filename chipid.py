from machine import unique_id

def chipid():
    _chipid = ''
    _uid = unique_id()
    for _v in _uid:
        _chipid += str(_v)
    return _chipid