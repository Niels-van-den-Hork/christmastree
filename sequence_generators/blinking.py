from typing import List, Iterator
from sequence_generators import SequenceGenerator
from data_structures import *


class BlinkingSequence(SequenceGenerator):
    framerate = 10 

    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.is_on = True

    def step(self, dt: float) -> Iterator[LED]:
        self.is_on = not self.is_on

        for led in self.led_list:
            led = led.get_led_with_new_color(RGB.RANDOM) 
            yield led