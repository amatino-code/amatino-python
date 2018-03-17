"""
Amatino API Python Bindings
New Transaction Arguments Module
Author: hugh@amatino.io

This module is intended to be private, used indirectly
by public classes, and should not be used directly.
"""
from datetime import datetime
from amatino.entry import Entry
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit
from amatino._internal._data_package import _DataPackage
from amatino._internal._am_time import _AMTime

class _NewTransactionArguments(_DataPackage):
    """
    Private - Not intended to be used directly.

    Used by instances of class Transaction to validate
    and hold new transaction arguments.
    """

    _INVALID_NEW_MESSAGE = """
        Invalid arguments for the initialisation of a new Transaction
    """
    _NO_TX_ID_MESSAGE = """
        A new Transaction must be initialised with transaction_id=None
    """
    _DATETIME_MESSAGE = """
        Argument "transaction_time" must be of type datetime.datetime when
        creating a new Transaction.
    """
    _GLOBAL_UNIT_TYPE_MESSAGE = """
        Global unit must be of type amatino.global_unit.GlobalUnit or None
    """
    _CUSTOM_UNIT_TYPE_MESSAGE = """
        Global unit must be of type amatino.global_unit.GlobalUnit or None
    """
    _DUAL_UNIT_MESSAGE = """
        Specify at least one of global_unit OR custom_unit, but not both.
    """
    _ENTRY_LIST_MESSAGE = """
        Entries must be supplied as members of a List.
    """
    _ENTRY_MESSAGE = """
        Entries must be of instances of the Entry class
    """
    _REQUIRED_DESCRIPTION_TYPE = """
        Transaction description must be of type str
        """

    def __init__(
            self,
            transaction_time: datetime = None,
            description: str = None,
            global_unit: GlobalUnit = None,
            custom_unit: CustomUnit = None,
            entries: [Entry] = None
        ):

        super().__init__()

        self._transaction_time = transaction_time
        self._description = description
        self._global_unit = global_unit
        self._custom_unit = custom_unit
        self._entries = entries

        if not isinstance(self._transaction_time, datetime):
            raise TypeError(self._DATETIME_MESSAGE)

        if not isinstance(self._description, str):
            raise TypeError(self._REQUIRED_DESCRIPTION_TYPE)

        if (
                self._global_unit is not None
                and not isinstance(self._global_unit, GlobalUnit)
        ):
            raise TypeError(self._GLOBAL_UNIT_TYPE_MESSAGE)

        if (
                self._custom_unit is not None
                and not isinstance(self._custom_unit, CustomUnit)
        ):
            raise TypeError(self._CUSTOM_UNIT_TYPE_MESSAGE)

        if self._custom_unit is not None and self._global_unit is not None:
            raise ValueError(self._DUAL_UNIT_MESSAGE)

        if self._custom_unit is None and self._global_unit is None:
            raise ValueError(self._DUAL_UNIT_MESSAGE)

        if not isinstance(self._entries, list):
            raise TypeError(self._ENTRY_LIST_MESSAGE)

        if False in [isinstance(e, Entry) for e in self._entries]:
            raise TypeError(self._ENTRY_MESSAGE)

        c_unit = None
        g_unit = None

        if self._custom_unit is not None:
            c_unit = self._custom_unit.code()
        if self._global_unit is not None:
            g_unit = self._global_unit.code()

        self._package = {
            'transaction_time': _AMTime(self._transaction_time).time(),
            'description': self._description,
            'global_unit': g_unit,
            'custom_unit': c_unit,
            'entries': [e.as_dict() for e in self._entries]
        }

        return
