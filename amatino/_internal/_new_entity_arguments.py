"""
Amatino API Python Bindings
New Entity Arguments Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
import json

class _NewEntityArguments:
    """
    Private - Not intended to be used directly.

    Used by instances of class Entity to validate, store, and
    process arguments for the creation of new Entities.
    """
    def __init__(
            self,
            entity_id: str,
            name: str,
            description: str,
            region: str
    ):

        raise NotImplementedError
