import pytest
from PIL import Image

FRONT_PATH = "tests/assets/tree_front.png"


@pytest.fixture
def front_image():
    return Image.open(FRONT_PATH)


RIGHT_PATH = "tests/assets/tree_right.png"


@pytest.fixture
def right_image():
    return Image.open(RIGHT_PATH)
