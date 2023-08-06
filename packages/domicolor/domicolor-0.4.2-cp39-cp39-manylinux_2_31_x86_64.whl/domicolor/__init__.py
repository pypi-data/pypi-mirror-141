from PIL import Image
import domicolor_backend
import numpy as np

from . import version
__version__ =version.version



def get_dominant_color(image, quality):
    """Get the dominant color.
    :param image: input image can be: 
                  1) numpy array in RGBA format
                  2) filename
                  3) BytesIO
    :param quality: quality settings, 1 is the highest quality, the bigger
                    the number, the faster a color will be returned but
                    the greater the likelihood that it will not be the
                    visually most dominant color
    :return tuple: (r, g, b)
    """
    palette = get_palette(image, 5, quality)
    return palette[0]


def get_palette(image, color_count=10):
    """Build a color palette.
        :param image: input image can be: 
                    1) numpy array in RGB format
                    2) filename
                    3) BytesIO
        :param color_count: number of colors in the palette
        :return list: a list of tuple in the form ((r, g, b), portion of color)
    """
    if not isinstance(image, np.ndarray):
        image = Image.open(image)
        image = image.convert('RGBA')
        image = np.array(image).astype(np.uint8)
        
    return domicolor_backend.get_palette(image, color_count)