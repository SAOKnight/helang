from typing import *
from helang.tokens import TYPES


class Value:
    def __init__(self, value_type: str, value: Optional[List[int]] = None):
        if value_type not in TYPES:
            raise TypeError('YOU CANNOT FIND ANOTHER TYPE.')
        self.value = value


class Env:
    def __init__(self, base: Optional['Env'] = None):
        self._base = base
        self._data = dict()

    def define(self, key: str, val: Value):
        self._data[key] = val

    def set(self, key: str, val: Value):
        # Find in bases
        cur = self
        while cur:
            if key in cur._data.keys():
                cur._data[key] = val
                break
            cur = cur._base
        else:
            self._data[key] = val

    def get(self, key: str) -> Value:
        val = self._data.get(key)
        if val is None:
            if self._base is not None:
                return self._base.get(key)
            else:
                return Value('void')
        return val
