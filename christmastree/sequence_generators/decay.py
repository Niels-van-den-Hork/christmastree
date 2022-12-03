from typing import List, Iterator
from christmastree.sequence_generators import SequenceGenerator
from christmastree.data_structures import *


class DecaySequence(SequenceGenerator):
    framerate = 30

    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.setup()

    def setup(self):
        self.colors = [RGB.RANDOM, RGB.RANDOM]
        self.time = 15

    def step(self, dt: float) -> Iterator[LED]:
        if self.time < 0:
            self.setup()
        self.time -= dt

        new_led_list = []
        for led in self.led_list:

            if random.uniform(0, 1) > 0.97:
                led = led.get_led_with_new_color(self.colors[1])
            else:
                led = led.get_led_with_new_color(led.color)

            new_led_list.append(led)
            yield led
        self.led_list = new_led_list
