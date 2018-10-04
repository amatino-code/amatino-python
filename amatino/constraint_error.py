"""
Amatino API Python Bindings
Constraint Error Module
Author: hugh@amatino.io
"""
from amatino.amatino_error import AmatinoError


class ConstraintError(AmatinoError):
    """
    A class of errors thrown when input data violates some constraint. For
    example, an Entity name that is too long.
    """
    pass
