from typing import Iterator

from PIL import Image
from PIL.Image import Image as PILImage

from data_structures import points


def _point_generator(width: int, height: int) -> Iterator[points.Point2D]:
    for x in range(width):
        for y in range(height):
            yield points.Point2D(x, y)


def _locate_led_in_image(image: PILImage) -> points.Point2D:
    image = image.convert(
        "L"
    )  # ITU-R 601-2 luma transform to get brightness of each pixel
    width, height = image.size
    max_brightness = -1e6
    max_point = points.Point2D(-1, -1)

    for point in _point_generator(width, height):
        brightness = image.getpixel(point)
        if brightness > max_brightness:
            max_brightness = brightness
            max_point = point

    return max_point.invert_y(
        height
    )  # invert y such that the origin is in the bottom left corner


def _locate_led_in_image_file(imagepath: str) -> points.Point2D:

    with Image.open(imagepath) as image:
        return _locate_led_in_image(image)


def locate_led_in_images(front_image_file: str, right_image_file: str) -> points.Point3D:
    """returns the 3d location of the led in the images

    output is relative to the two camera positions.
    this output should be mapped to a unit box, as such camera position or zoom is not needed to be precise.

    front.y and right.y are likely somewhat similar, but any offset that would exist is constant and as such not important?
    """

    front = _locate_led_in_image_file(front_image_file)  # x => x, y => z
    right = _locate_led_in_image_file(right_image_file)  # x => y, y => z

    return points.Point3D(front.x, front.y, right.x)
