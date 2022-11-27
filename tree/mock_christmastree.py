import math
import random
from queue import Queue
from typing import Iterator, List

from matplotlib import animation, collections
from matplotlib import pyplot as plt
import matplotlib
import numpy as np

# matplotlib.use('Agg')

from data_structures import led, rgb, points

MIN_LAYER = 1
MAX_LAYER = 9
MAX_RADIUS = 2
TOTAL_LAYERS = MAX_LAYER - MIN_LAYER


class MockChristmasTree:
    def __init__(self, num_steps: int, framerate: int):
        self.num_steps = num_steps
        self.framerate = framerate

    def visualize(self, queue: Queue[List[led.LED]], is_interactive=False):

        fig = plt.figure(figsize=(10, 8))

        ax = plt.subplot2grid((2, 2), (0, 0), projection="3d", rowspan=2)
        ax = self._set_axis(ax)

        ax2 = plt.subplot2grid((2, 2), (0, 1))
        ax3 = plt.subplot2grid((2, 2), (1, 1))
        # ax = self._set_axis(ax)

        plt_points = self._initialise(queue, ax, ax2, ax3)

        ani = animation.FuncAnimation(
            fig=fig,
            func=self._update,
            frames=self.num_steps,
            fargs=(queue, plt_points),
            interval=1 / self.framerate,
            blit=False,
        )

        if is_interactive:
            plt.show()
        else:
            ani.save(
                "matplot003.mp4", writer=animation.FFMpegWriter(fps=self.framerate)
            )
        # plt.close()

    @staticmethod
    def create_led_in_cone_shape(num_leds=50) -> Iterator[led.LED]:
        for index, point in enumerate(_generate_points_in_cone(num_leds)):
            yield led.LED(led.LedIdentifier(index), point, rgb.RGB.RANDOM)

    def _set_axis(self, ax):
        # Setting the axes properties
        ax.set_xlim3d([-5, 5])  # type: ignore
        ax.set_xlabel("X")

        ax.set_ylim3d([-5, 5])  # type: ignore
        ax.set_ylabel("Y")

        ax.set_zlim3d([0, 10.0])  # type: ignore
        ax.set_zlabel("Z")  # type: ignore
        return ax

    def _initialise(
        self, queue: Queue, ax: plt.Axes, ax2: plt.Axes, ax3: plt.Axes
    ) -> List[collections.PathCollection]:
        led_list = queue.get()
        xs, ys, zs, cs, phis = _get_plt_points_from_leds(led_list)

        new_phis = list(_calculate_new_phis(phis, zs))

        return [
            ax.scatter(xs, ys, zs, c=cs, alpha=0.8, linewidths=4),
            ax2.scatter(phis, zs, c=cs),
            ax3.scatter(new_phis, zs, c=cs),
        ]

    def _update(
        self,
        num,
        queue: Queue,
        plt_points: List[collections.PathCollection],
    ):
        led_list = queue.get()

        _, _, _, cs, _ = _get_plt_points_from_leds(led_list)

        for plt_point in plt_points:
            plt_point.set_color(cs)
        return plt_points


def _get_plt_points_from_leds(led_list: List[led.LED]):
    """extract required data from led list to plot"""

    xs = []
    ys = []
    zs = []
    cs = []
    phis = []
    for point in led_list:
        xs.append(point.location.x)
        ys.append(point.location.y)
        zs.append(point.location.z)
        cs.append(point.color.rgb_zero_to_one)
        phis.append(point.location.phi)
    return xs, ys, zs, cs, phis


def _rand(vmin: float = 0, vmax: float = 10) -> float:
    return random.uniform(vmin, vmax)


def abs(x):
    return x if x > 0 else -x


def _nudge_clip(value, vmin: float, vmax: float) -> float:
    e = 0.1
    if value < vmin:
        value = vmin + abs(vmin - value) + e
    if value > vmax:
        value = vmax - abs(value - vmax) - e
    return value


def _clip(value, vmin: float, vmax: float) -> float:
    return max(min(value, vmax), vmin)


def _rand_layer(n=1, vmin=0, vmax=10) -> float:
    """weighted such that it produces a conical distribution"""
    samples = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    weights = [9, 8, 7, 6, 5, 4, 3, 2, 1]

    layer = random.choices(samples, weights)[0]
    layer += _rand(-0.5, 0.5)
    layer = _clip(layer, 1, 9)
    return layer


def _generate_points(n=50) -> Iterator[points.Point3D]:
    for _ in range(n):
        yield points.Point3D(_rand(), _rand(), _rand())


def _get_radius_at_layer(layer: float) -> float:
    if not (MIN_LAYER <= layer <= MAX_LAYER):
        raise ValueError("layer not in range [MIN_LAYER,MAX_LAYER]")

    return MAX_RADIUS - (layer - 1) / 4


def _generate_points_in_cone(n=50) -> Iterator[points.Point3D]:
    for _ in range(n):
        layer = _rand_layer(1, 9)  # should be weighted to be low
        radius = _get_radius_at_layer(layer)
        angle = _rand(0, 360)

        yield points.Point3D(radius * math.cos(angle), radius * math.sin(angle), layer)


def _calculate_new_phi(phi: float, z: float) -> float:

    MIN_LAYER = 1
    MAX_LAYER = 9
    MAX_RADIUS = 2
    TOTAL_LAYERS = MAX_LAYER - MIN_LAYER

    def safe_div(a, b):
        if b == 0:
            return 0
        else:
            return a / b

    def _get_radius_at_layer(layer: float) -> float:
        if not (MIN_LAYER <= layer <= MAX_LAYER):
            raise ValueError("layer not in range [MIN_LAYER,MAX_LAYER]")

        return MAX_RADIUS - (layer - 1) / 4

    def _correction(layer):
        if not (MIN_LAYER <= layer <= MAX_LAYER):
            raise ValueError("layer not in range [MIN_LAYER,MAX_LAYER]")

        return 1 + (layer * TOTAL_LAYERS / points.PI)

    return safe_div((phi - (points.PI / 2)), (_get_radius_at_layer(z))) * _correction(z)


def _calculate_new_phis(phis: List[float], zs: List[float]) -> Iterator[float]:
    for phi, z in zip(phis, zs):
        yield _calculate_new_phi(phi, z)
