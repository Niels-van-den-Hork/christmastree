from __future__ import annotations

import random
from typing import NamedTuple, NewType, Any, List

class RGB(NamedTuple):
    red: int
    green: int
    blue: int
    alpha: int = 100

    @classmethod
    @property
    def ON(cls):
        return cls(255, 255, 255, 100)

    @classmethod
    @property
    def OFF(cls):
        return cls(0, 0, 0, 100)

    @classmethod
    @property
    def RED(cls):
        return cls(255, 0, 0, 100)

    @classmethod
    @property
    def GREEN(cls):
        return cls(0, 255, 0, 100)

    @classmethod
    @property
    def BLUE(cls):
        return cls(0, 0, 255, 100)

    @classmethod
    @property
    def RANDOM(cls):
        def rand() -> int:
            return int(random.uniform(0, 255))

        return cls(rand(), rand(), rand(), 100)

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)

    @property
    def rgb_zero_to_one(self):
        return (self.red / 255, self.green / 255, self.blue / 255)



