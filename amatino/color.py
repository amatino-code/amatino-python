"""
Amatino API Python Bindings
Color Module
Author: hugh@amatino.io
"""
from typing import TypeVar
from typing import Type
from amatino.internal.immutable import Immutable

T = TypeVar('T', bound='Color')


class Color:
    """
    A representation of an RGB color.
    """
    def __init__(
        self,
        red: int,
        green: int,
        blue: int
    ) -> None:

        if (
                not isinstance(red, int)
                or not isinstance(green, int)
                or not isinstance(blue, int)
        ):
            raise TypeError('Color components must be of type int')

        if (
                red < 0 or red > 255 or
                green < 0 or green > 255 or
                blue < 0 or blue > 255
        ):
            raise ValueError('Color components must be >= 0 and <= 255')

        self._red = red
        self._green = green
        self._blue = blue

        return

    red: int = Immutable(lambda s: s._red)
    green: int = Immutable(lambda s: s._green)
    blue: int = Immutable(lambda s: s._blue)

    @classmethod
    def from_hex_string(cls: Type[T], hexstring: str) -> T:

        if not isinstance(hexstring, str):
            raise TypeError('hexstring must be of type `str`')

        if len(hexstring) != 6:
            raise ValueError('hexstring must be 6 characters')

        red = int(hexstring[:2], 16)
        green = int(hexstring[2:4], 16)
        blue = int(hexstring[4:6], 16)

        color = cls(red=red, green=green, blue=blue)

        return color

    def as_hex_string(self) -> str:
        """
        Return the colour as a hex value string
        """
        raise NotImplementedError

    def as_int_tuple(self) -> tuple:
        """
        Return the colour as a tuple of three integers, in the order
        (red, green, blue)
        """
        return (self._red, self._green, self._blue)
