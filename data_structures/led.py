from __future__ import annotations
from data_structures import points, rgb
from typing import NewType, List

LedIdentifier = NewType("LedIdentifier", int)

class LED:
    def __init__(
        self,
        index: LedIdentifier,
        location: points.Point3D,
        color: rgb.RGB,
        neighbours: List[LED] = [],
    ):
        self._index = index
        self._location = location
        self._color = color
        self.neighbours = neighbours.copy()

    @property
    def index(self) -> LedIdentifier:
        return self._index

    @property
    def location(self) -> points.Point3D:
        return self._location

    @property
    def color(self) -> rgb.RGB:
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def copy(self) -> LED:
        return LED(self._index, self._location, self.color, [])

    def get_led_with_new_color(self, color: rgb.RGB) -> LED:
        return LED(self._index, self._location, color, self.neighbours)


def connected_leds(led_list: List[LED]):
    for led in led_list:
        mutable_list = led_list.copy()
        mutable_list.sort(key=lambda led2: led.location.get_distance(led2.location))

        led.neighbours.append(mutable_list[1])

        if led.location.get_distance(mutable_list[2].location) < 0.3:
            led.neighbours.append(mutable_list[2])

        if led.location.get_distance(mutable_list[3].location) < 0.3:
            led.neighbours.append(mutable_list[3])
