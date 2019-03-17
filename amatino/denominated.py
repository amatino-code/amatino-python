"""
Amatino API Python Bindings
Denominated Module
Author: hugh@amatino.io
"""
from amatino.denomination import Denomination
from amatino.custom_unit import CustomUnit
from amatino.global_unit import GlobalUnit
from amatino.internal.immutable import Immutable
from amatino.entity import Entity
from typing import TypeVar

T = TypeVar('T', bound='Denominated')


class Denominated:
    """
    Abstract class defining an interface for objects that are
    denominated in an Amatino unit of account, i.e. in a Custom Unit or
    Global Unit. Provides default functionality for determining what
    unit denominates an object. Provides default caching capacity
    for retrieved Custom Units and Global Units such that repeated requests
    for them from properties will not result in extra synchronous calls
    to the Amatino API
    """

    global_unit_id = NotImplemented
    custom_unit_id = NotImplemented
    denomination = Immutable(lambda s: s._denomination())
    entity = NotImplemented

    _denominated_cached_custom_unit = None
    _denominated_cached_global_unit = None

    def _denomination(self) -> Denomination:
        """Return the unit denominating this object"""
        if self.global_unit_id == NotImplemented:
            raise NotImplementedError('Implement .global_unit_id property')
        if self.custom_unit_id == NotImplemented:
            raise NotImplementedError('Implement .custom_unit_id property')
        if not isinstance(self.entity, Entity):
            raise NotImplementedError('Implement .entity property')

        if self.global_unit_id is not None and self.custom_unit_id is not None:
            raise AssertionError('Both global & custom units supplied!')

        if self.global_unit_id is not None:
            assert isinstance(self.global_unit_id, int)
        if self.custom_unit_id is not None:
            assert isinstance(self.custom_unit_id, int)

        if self.global_unit_id is not None:
            assert isinstance(self.global_unit_id, int)
            if self._denominated_cached_global_unit is not None:
                return self._denominated_cached_global_unit
            global_unit = GlobalUnit.retrieve(
                self.entity.session,
                self.global_unit_id
            )
            self._denominated_cached_global_unit = global_unit
            return global_unit

        if self._denominated_cached_custom_unit is not None:
            return self._denominated_cached_custom_unit
        custom_unit = CustomUnit.retrieve(
            self.entity,
            self.entity.session,
            self.custom_unit_id
        )
        self._denominated_cached_custom_unit = custom_unit
        return custom_unit
