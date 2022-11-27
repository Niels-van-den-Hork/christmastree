
from typing import List, Iterator
from sequence_generators import SequenceGenerator
from data_structures import *




class GraphWalkSequence(SequenceGenerator):
    framerate = 30
    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.setup()

    def setup(self):
        self.led = self.led_list[0]
        self.prev_led = self.led
        
        for led in self.led_list:
            led.color = RGB.OFF

    def step(self, dt: float) -> Iterator[LED]:
        
        self.prev_led.color = RGB.OFF
        self.led.color = RGB.ON

        self.prev_led = self.led
        led_index = random.choice(self.led.neighbours).index
        self.led = self.led_list[led_index]

        for led in self.led_list:
            yield led

