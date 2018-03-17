"""
Amatino API Python Bindings
Region Module
Author: hugh@amatino.io
"""
from amatino.session import Session

class Region:
    """
    A geographic region in which Amatino can store accounting information.
    """
    def __init__(self, region_code: str, session: Session):
        raise NotImplementedError
