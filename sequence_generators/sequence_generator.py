from typing import List, Iterator

from data_structures import *
from abc import ABC, abstractmethod
import random

class SequenceGenerator(ABC):
    framerate : int
    
    def __init__(self, led_list: Iterator[LED]) -> None:
        self.led_list = list(led_list)

    @abstractmethod
    def step(self, dt: float) -> Iterator[LED]:
        raise NotImplementedError

