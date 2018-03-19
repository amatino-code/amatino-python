"""
Amatino API Python Bindings
Url Target Module
Author: hugh@amatino.io
"""

class _UrlTarget:
    """
    Internal class handling individual url parameter
    components
    """
    def __init__(self, key: str, value: str):

        assert isinstance(key, str)
        if (
                not isinstance(value, str)
                and not isinstance(value, int)
            
            ):
            raise AssertionError('Value must be of type int or str')

        self.key = key
        self.value = value

    def __str__(self):
        return self.key + '=' + str(self.value)

    def __eq__(self, other):
        if (
                other.key == self.key
                and other.value == self.value
        ):
            return True
        return False
