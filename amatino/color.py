"""
Amatino API Python Bindings
Color Module
Author: hugh@amatino.io
"""

class Color:
    """
    A representation of an RGB color.
    """
    def __init__(
        self,
        red: int,
        green: int,
        blue: int
    ):

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
