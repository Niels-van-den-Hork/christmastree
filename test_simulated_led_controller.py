from typing import List

from sequence_generators import *
from main import animate

import pytest


@pytest.mark.parametrize(
    "is_interactive,is_multithreading",
    [
        (True, True),
        (True, False),
        (False, False),
        (False, True),
    ],
)
def test_animate(is_interactive: bool, is_multithreading: bool):
    animate(DecaySequence, is_interactive, is_multithreading, num_steps=100, num_leds = 100)
