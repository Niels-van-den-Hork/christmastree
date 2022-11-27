from queue import Queue
from typing import List, Iterator, Optional

from data_structures import led
from tree.abstract_controller import Controller

from tree.mock_christmastree import MockChristmasTree

import threading
import matplotlib.pyplot as plt


class MockController(Controller):
    """handles multithreading communication with the mock christmastree"""

    def __init__(
        self,
        mock_christmas_tree: MockChristmasTree,
        is_interactive: bool = True,
        is_multithreading: bool = False,
    ):
        self._queue: Queue[List[led.LED]] = Queue()
        self._tree = mock_christmas_tree
        self._is_interactive = is_interactive
        self._is_multithreading = is_multithreading

        self.visualisation_thread = threading.Thread(
            target=mock_christmas_tree.visualize, args=(self._queue, is_interactive)
        )

    def pre_run(self):
        if self._is_multithreading:
            self.visualisation_thread.start()

    def post_run(self):
        if self._is_multithreading:
            self.visualisation_thread.join()
        else:
            self._tree.visualize(self._queue, self._is_interactive)

    def set_led_state(self, led_state: led.LED) -> None:
        raise ValueError("use set_multiple_led_states on mock controller for now")

    def set_multiple_led_states(self, led_states: Iterator[led.LED]) -> None:
        self._queue.put(list(led_states))
