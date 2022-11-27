import os
from typing import Type

# import led_registration
# from camera import Camera
from sequence_generators.sequence_generator import SequenceGenerator
from tree.abstract_controller import Controller
from tree.mock_controller import MockController
from tree.mock_christmastree import MockChristmasTree

# there can be two views on the positions:
# 1. A led has a posistion
# 2. A position could have a led

# the first view is simple to programm, but could be slower
# The second view would be more suitable to programm sequences for, but is more complicated to programm
# we could still write sequences in the second view, and convert to the first view. which may be easier than the other way around.


PATH_FRONT_IMAGE = os.path.join("images", "front")
PATH_RIGHT_IMAGE = os.path.join("images", "right")

"""
def register_led_positions():
    camera = Camera()
    led_controller = TreeController()
    led_registration.register_led_positions(
        "locations.pickle", camera, led_controller, 50
    )

"""
# convert list of positions to list of LEDs
# LED(LedIdentifier(i), loc, RGB.OFF) for i, loc in enumerate(locations)


def animate(
    sequence_type: Type[SequenceGenerator],
    is_interactive: bool = True,
    is_multithreading: bool = True,
    num_steps: int = 1000,
    num_leds: int = 250
) -> None:

    locations = MockChristmasTree.create_led_in_cone_shape(num_leds)

    sequence = sequence_type(locations)
    # connected_leds(sequence.led_list)
    tree = MockChristmasTree(num_steps - 5, sequence.framerate)

    controller = MockController(tree, is_interactive, is_multithreading)

    controller.pre_run()
    _run_sequence(controller, sequence, num_steps)
    controller.post_run()


def _run_sequence(
    controller: Controller, sequence_generator: SequenceGenerator, num_steps=5
):
    for _ in range(num_steps):
        dt = 0.1  # change to time passed since last iteration
        led_states = sequence_generator.step(dt)
        controller.set_multiple_led_states(led_states)
