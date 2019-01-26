import random
import string

from imagekit import ImageSpec
from imagekit.processors import ResizeToFill


class ProfilePictureThumbnail(ImageSpec):
    processors = [ResizeToFill(300, 300)]
    format = 'JPEG'
    options = {'quality': 100}


class AvatarThumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 80}


def generate_resized_profile_picture(picture):
    try:
        image_generator = ProfilePictureThumbnail(source=picture)
        result = image_generator.generate()
        dest = open(picture.path, mode='bw')
        dest.write(result.read())
        dest.close()

    except:
        return False


def generate_avatar(picture):
    try:
        image_generator = AvatarThumbnail(source=picture)
        result = image_generator.generate()
        dest = open(picture.path, mode='bw')
        dest.write(result.read())
        dest.close()

    except:
        return False


def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
