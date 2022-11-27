from abc import ABC, abstractmethod
from typing import Iterator

from data_structures import led, rgb, points


class Controller(ABC):
    @abstractmethod
    def set_led_state(self, led_state: led.LED) -> None:
        raise NotImplementedError

    def turn_on_led(self, index: led.LedIdentifier) -> None:
        state = led.LED(index, points.Point3D.ZERO, rgb.RGB.ON)
        self.set_led_state(state)

    def turn_off_led(self, index: led.LedIdentifier) -> None:
        state = led.LED(index, points.Point3D.ZERO, rgb.RGB.OFF)
        self.set_led_state(state)

    def set_multiple_led_states(self, led_states: Iterator[led.LED]) -> None:
        for state in led_states:
            self.set_led_state(state)
