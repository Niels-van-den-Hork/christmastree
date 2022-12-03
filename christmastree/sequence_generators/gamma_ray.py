from typing import List, Iterator
from christmastree.sequence_generators import SequenceGenerator
from christmastree.data_structures import *


class GammaRaySequence(SequenceGenerator):
    framerate = 30

    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.setup()

    def setup(self):
        self.colors = [RGB.RANDOM, RGB.RANDOM]
        self.dot = Point2D_Float(0.0, 9.0)
        self.vel = random.uniform(-0.1, 0.1)
        self.first = True

    def step(self, dt: float) -> Iterator[LED]:
        if self.dot.y < 0:
            self.setup()

        self.dot = Point2D_Float(self.dot.x + self.vel, self.dot.y - dt)
        new_led_list = []
        for led in self.led_list:
            projected = Point2D_Float(led.location.corrected_phi, led.location.z)
            if projected.get_distance(self.dot) < 1:
                led = led.get_led_with_new_color(self.colors[0])
            else:
                if self.first or random.uniform(0, 1) > 0.8:
                    led = led.get_led_with_new_color(self.colors[1])
                else:
                    led = led.get_led_with_new_color(led.color)
            new_led_list.append(led)
            yield led
        self.first = False
        self.led_list = new_led_list
