from typing import List, Iterator
from christmastree.sequence_generators import ElevatorSequence
from christmastree.data_structures import *


class SpiralElevatorSequence(ElevatorSequence):
    framerate = 3

    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.colors = [
            RGB.RANDOM,
            RGB.RANDOM,
            RGB.RANDOM,
            RGB.RANDOM,
            RGB.RANDOM,
            RGB.RANDOM,
            RGB.RANDOM,
        ]

    def inc_bar(self, bar):
        bar = bar + 0.21
        if bar > 2:
            bar = 0
            self.colors.append(RGB.RANDOM)
            self.colors.pop(0)
        return bar

    def step(self, dt: float) -> Iterator[LED]:
        self.bar = self.inc_bar(self.bar)

        for led in self.led_list:

            led = led.get_led_with_new_color(self.colors[5])
            if self.bar - 3 < led.location.z + 4 * (led.location.phi - 1):
                led = led.get_led_with_new_color(self.colors[4])

            if self.bar < led.location.z + 4 * (led.location.phi - 1):
                led = led.get_led_with_new_color(self.colors[3])

            if self.bar + 3 < led.location.z + 4 * (led.location.phi - 1):
                led = led.get_led_with_new_color(self.colors[2])

            if self.bar + 6 < led.location.z + 4 * (led.location.phi - 1):
                led = led.get_led_with_new_color(self.colors[1])

            if self.bar + 9 < led.location.z + 4 * (led.location.phi - 1):
                led = led.get_led_with_new_color(self.colors[0])

            yield led
