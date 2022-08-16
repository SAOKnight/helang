from enum import Enum


class Methods:
    def __init__(self):
        self._methods = dict()

    def bind(self, enum: Enum):
        def bind_method(method: callable):
            self._methods[enum] = method
            return method
        return bind_method

    def apply(self, enum: Enum, *args, **kwargs):
        return self._methods[enum](*args, **kwargs)
