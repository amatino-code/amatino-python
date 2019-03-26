"""
Amatino API Python Bindings
State Module
Author: hugh@amatino.io
"""
from enum import Enum


class State(Enum):
    ALL = 'all'
    ACTIVE = 'active'
    DELETED = 'deleted'
