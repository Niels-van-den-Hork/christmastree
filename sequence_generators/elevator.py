from typing import List, Iterator
from sequence_generators import SequenceGenerator
from data_structures import *



class ElevatorSequence(SequenceGenerator):
    framerate = 30 
    def __init__(self, locations: Iterator[LED]) -> None:
        super().__init__(locations)
        self.colors = [RGB.RANDOM,RGB.RANDOM,RGB.RANDOM]
        self.bar = 1
        self.bar2 = 5

    def inc_bar(self,bar):
        bar = bar + 0.21
        if bar > 4:
            bar = 0
            self.colors.append(RGB.RANDOM)
            self.colors.pop(0)
        return bar

    def step(self, dt: float) -> Iterator[LED]:
        self.bar = self.inc_bar(self.bar)

        for led in self.led_list:
            
            led =  led.get_led_with_new_color(self.colors[2])

            if self.bar < led.location.z:
                led = led.get_led_with_new_color(self.colors[1]) 

            if self.bar + 4 < led.location.z:
                led = led.get_led_with_new_color(self.colors[0]) 


            yield led