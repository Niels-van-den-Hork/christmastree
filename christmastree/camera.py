import io
from time import sleep
from typing import Tuple

from PIL import Image
from PIL.Image import Image as PILImage

from libs.picamera import PiCamera


class Camera:
    def __init__(self, resolution: Tuple[int, int] = (1024, 768)) -> None:
        self.camera = PiCamera()
        self.camera.resolution = resolution

    def capture_to_file(self, filename: str = "latest_image.jpg") -> None:
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture(filename)

    def capture_to_image(self) -> PILImage:
        stream = io.BytesIO()
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture(stream, fomrat="jpeg")
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        return Image.open(stream)
