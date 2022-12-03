from typing import List

from christmastree.data_structures import led, rgb, points
from christmastree.tree.abstract_controller import Controller


class TreeController(Controller):
    def __init__(self):
        pass

    def set_led_state(self, led_state: led.LED) -> None:
        pass
