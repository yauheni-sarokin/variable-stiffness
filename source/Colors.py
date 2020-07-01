from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import List


class ColorGradients(Enum):
    BY_DESIGN = {'name': 'by design', 'start': '#009FFF', 'end': '#ec2F4B'}
    VICE_CITY = {'name': 'vice city', 'start': '#3494E6', 'end': '#EC6EAD'}
    TIMBER = {'name': 'timber', 'start': '#fc00ff', 'end': '#00dbde'}
    MIAKA = {'name': 'timber', 'start': '#0ABFBC', 'end': '#FC354C'}
    REA = {'name': '#FFE000', 'start': '#FFE000', 'end': '#799F0C'}
    GREEN_RED = {'name': 'timber', 'start': '#00AB08', 'end': '#BB0103'}


class Color(ABC):
    pass


class RGBColor(Color):

    def __init__(self, rgb_color: List[int]) -> None:
        self._rgb_ = rgb_color

    @property
    def rgb(self):
        return self._rgb_

    def to_hex(self) -> HEXColor:
        rgb_color_ = [int(x) for x in self._rgb_]
        hex_color_ = "#" + "".join(["0{0:x}".format(v) if v < 16 else
                                    "{0:x}".format(v) for v in rgb_color_])
        return HEXColor(hex_color_)

    def __str__(self):
        return ','.join([str(i) for i in self._rgb_])


class HEXColor(Color):

    def __init__(self, hex_: str) -> None:
        self._hex_ = hex_

    @property
    def hex(self):
        return self._hex_

    def to_rgb(self) -> RGBColor:
        rgb_color_ = [int(self._hex_[i:i + 2], 16) for i in range(1, 6, 2)]
        return RGBColor(rgb_color_)

    def __str__(self):
        return self._hex_


def hex_to_RGB(hex):
    """
    "#FFFFFF" -> [255,255,255]
    :param hex:
    :return:
    """
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i + 2], 16) for i in range(1, 6, 2)]


def RGB_to_hex(RGB):
    """
    [255,255,255] -> "#FFFFFF"
    :param RGB:
    :return:
    """
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#" + "".join(["0{0:x}".format(v) if v < 16 else
                          "{0:x}".format(v) for v in RGB])


def color_dict(gradient):
    """
    Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on
    :param gradient:
    :return:
    """
    return {"hex": [RGB_to_hex(RGB) for RGB in gradient],
            "r": [RGB[0] for RGB in gradient],
            "g": [RGB[1] for RGB in gradient],
            "b": [RGB[2] for RGB in gradient]}


# Use this function to obtain linear gradient between two colors
def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    """
    returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    including the number sign ("#FFFFFF")
    :param start_hex:
    :param finish_hex:
    :param n:
    :return:
    """
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initialize a list of the output colors with the starting color
    RGB_list = [s]
    # Calculate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
            int(s[j] + (float(t) / (n - 1)) * (f[j] - s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)

def get_color_gradient_array(n:int,
                             color_gradient: ColorGradients = ColorGradients.VICE_CITY):
    start_ = color_gradient.value['start']
    end_ = color_gradient.value['end']

    gradient = linear_gradient(start_, end_, n)

    return gradient['hex']
