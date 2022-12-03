import os
import pickle
from typing import List, Tuple

import image_processing
from camera import Camera
from christmastree.data_structures import led, points
from christmastree.tree.tree_controller import TreeController

# there can be two views on the positions:
# 1. A led has a posistion
# 2. A position could have a led

# the first view is simple to programm, but could be slower
# The second view would be more suitable to programm sequences for, but is more complicated to programm
# we could still write sequences in the second view, and convert to the first view. which may be easier than the other way around.


PATH_FRONT_IMAGE = os.path.join("images", "front")
PATH_RIGHT_IMAGE = os.path.join("images", "right")


def register_led_positions(
    filename: str, camera: Camera, led_controller: TreeController, num_leds: int
):
    _capture_to_file_all_leds(camera, led_controller, num_leds, PATH_FRONT_IMAGE)
    _wait_for_camera_moved()
    _capture_to_file_all_leds(camera, led_controller, num_leds, PATH_RIGHT_IMAGE)

    locations = _localise_all_leds()
    locations = _map_to_unit_box(locations)

    # something like that
    with open(filename, "rw") as file:
        pickle.dump(locations, file)


def _capture_to_file_all_leds(
    camera: Camera, led_controller: TreeController, num_leds: int, folderpath: str
):
    for led_index in range(num_leds):
        led_controller.turn_on_led(led.LedIdentifier(led_index))
        filepath = os.path.join(folderpath, f"{led_index}.jpg")
        camera.capture_to_file(filepath)


def _wait_for_camera_moved():
    pass


def _localise_all_leds() -> List[points.Point3D]:
    """origin is bottom left front corner in reference to the front position"""
    front_image_files = os.listdir(PATH_FRONT_IMAGE)
    right_image_files = os.listdir(PATH_RIGHT_IMAGE)
    assert len(front_image_files) == len(right_image_files)

    all_locations = []
    for front_image_file, right_image_file in zip(front_image_files, right_image_files):
        location = image_processing.locate_led_in_images(
            front_image_file, right_image_file
        )
        all_locations.append(location)

    return all_locations


def _get_bounding_box(
    locations: List[points.Point3D],
) -> Tuple[points.Point3D, points.Point3D]:
    min_x = min([loc.x for loc in locations])
    max_x = max([loc.x for loc in locations])
    min_y = min([loc.y for loc in locations])
    max_y = max([loc.y for loc in locations])
    min_z = min([loc.z for loc in locations])
    max_z = max([loc.z for loc in locations])

    min_point = points.Point3D(min_x, min_y, min_z)
    max_point = points.Point3D(max_x, max_y, max_z)
    return (min_point, max_point)


def _map_to_unit_box(locations: List[points.Point3D]) -> List[points.Point3D]:
    min_point, max_point = _get_bounding_box(locations)

    def scale_point_to_unit(point: points.Point3D) -> points.Point3D:
        return (point - min_point) // max_point

    locations = list(map(scale_point_to_unit, locations))
    return locations
