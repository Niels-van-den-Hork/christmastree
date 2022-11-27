import image_processing
from tests.conftest import FRONT_PATH, RIGHT_PATH, front_image


def approx_equals(a, b, e):
    return abs(a - b) < e


def test_locate_led_in_image(front_image):
    point = image_processing._locate_led_in_image(front_image)
    x, y = point
    epsilon = 10
    assert approx_equals(x, 333, epsilon)
    assert approx_equals(y, 298, epsilon)


def test_locate_led_in_images():
    point = image_processing.locate_led_in_images(FRONT_PATH, RIGHT_PATH)
