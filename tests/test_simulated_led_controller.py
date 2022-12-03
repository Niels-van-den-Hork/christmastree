from typing import List

from christmastree import sequence_generators
from christmastree import main

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
    main.animate(
        sequence_generators.DecaySequence,
        is_interactive,
        is_multithreading,
        num_steps=100,
        num_leds=100,
    )
