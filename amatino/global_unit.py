"""
Amatino API Python Bindings
Global Unit Module
Author: hugh@blinkybeach.com
"""

class GlobalUnit:
    """
    Global Units are standardised units of account available across
    all Amatino Entities. For example, major currencies are available
    as Global Units.
    """
    def __init__(self, unit_code: str):
        
        if not isinstance(unit_code, str):
            raise TypeError('unit_code must be of type str')

        raise NotImplementedError