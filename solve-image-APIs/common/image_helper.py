import hashlib
import base64

from PIL import Image
from io import BytesIO


def get_hash(a_string):
    return hashlib.md5(a_string.encode("utf-8")).hexdigest()


def encode_image_base64(raw_image):
    return "data:image/png;charset=utf-8;base64," + base64.b64encode(raw_image).decode("utf8")


def decode_image_base64(encoded_image):
    # get the encoded string past the headers
    encoded_string = encoded_image.split("base64,", 1)[1]
    return base64.b64decode(encoded_string)


def rotate_image(image_in_bytes, angle):
    image = Image.open(BytesIO(image_in_bytes))
    rotated_bytes = BytesIO()
    image.rotate(angle, expand=1).save(rotated_bytes, format='PNG')
    return rotated_bytes.getvalue()
