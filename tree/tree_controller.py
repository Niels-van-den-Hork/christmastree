from typing import List

from data_structures import led, rgb, points
from tree.abstract_controller import Controller


class TreeController(Controller):
    def __init__(self):
        pass

    def set_led_state(self, led_state: led.LED) -> None:
        pass
