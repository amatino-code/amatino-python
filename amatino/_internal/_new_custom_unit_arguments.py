"""
Amatino API Python Bindings
New Custom Unit Arguments
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from amatino._internal._data_package import _DataPackage

class _NewCustomUnitArguments(_DataPackage):
    """
    Private - Not intended to be used directly.

    Used by instances of class CustomUnit to validate arguments provided
    for the creation of a new Custom Unit
    """
    _REQUIRED_CODE_TYPE = 'Custom unit code must be of type str'
    _REQUIRED_CODE_LENGTH = """
        Custom unit code must be at least 3, and no more than 64,
        characters long.
        """
    _REQUIRED_NAME_TYPE = 'Custom unit name must be of type str'
    _REQUIRED_NAME_LENGTH = """
        Custom unit name must be no more than 1024 characters long
        """
    _REQUIRED_PRIORITY_TYPE = """
        Custom Unit priority must be of type None or int
        """
    _REQUIRED_PRIORITY_SIZE = """
        Custom Unit priority must be between -1,000 and 1,000, inclusive
        """
    _REQUIRED_DESCRIPTION_TYPE = """
        Custom Unit description must be of type str or None
        """
    _REQUIRED_DESCRIPTION_LENGTH = """
        Custom Unit description must be no more than 1024 characters long
        """
    _REQUIRED_EXPONENT_TYPE = """
        Custom Unit exponent must be of type int
        """
    _REQUIRED_EXPONENT_SIZE = """
        Custom Unit exponent must be greater than or equal to 0 and less
        than or equal to 6
        """

    def __init__(
            self,
            code: str,
            name: str,
            priority: int,
            description: str,
            exponent: int
        ):

        super().__init__()

        if not isinstance(code, str):
            raise TypeError(self._REQUIRED_CODE_TYPE)

        if len(code) > 64 or len(code) < 3:
            raise ValueError(self._REQUIRED_CODE_LENGTH)

        if not isinstance(name, str):
            raise TypeError(self._REQUIRED_NAME_TYPE)

        if len(name) > 1024:
            raise ValueError(self._REQUIRED_NAME_LENGTH)

        if priority is not None and not isinstance(priority, int):
            raise TypeError(self._REQUIRED_PRIORITY_TYPE)

        if (
                priority is not None
                and (
                    priority < -1000 or priority > 1000
                )
            ):
            raise ValueError(self._REQUIRED_PRIORITY_SIZE)

        if description is not None and not isinstance(description, str):
            raise TypeError(self._REQUIRED_DESCRIPTION_TYPE)

        if description is not None and len(description) > 1024:
            raise ValueError(self._REQUIRED_DESCRIPTION_LENGTH)

        if not isinstance(exponent, int):
            raise TypeError(self._REQUIRED_EXPONENT_TYPE)

        if exponent < 0 or exponent > 6:
            raise ValueError(self._REQUIRED_EXPONENT_SIZE)

        self._code = code
        self._name = name
        self._priority = priority
        self._description = description
        self._exponent = exponent

        self._package = {
            'code': self._code,
            'name': self._name,
            'pririty': self._priority,
            'description': self._description,
            'exponent': self._exponent
        }

        return
