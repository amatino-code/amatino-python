"""
Amatino API Python Bindings
Entity Test Module
Author: hugh@amatino.io
"""
from typing import Optional
from amatino.entity import Entity
from amatino.tests.ancillary.session import SessionTest


class EntityTest(SessionTest):
    """
    Test the Entity primary object
    """
    TEST_ALL_SESSION_METHODS = False

    def __init__(self, name='Create, retrieve an Entity') -> None:

        self.entity: Optional[Entity] = None

        super().__init__(name)
        result = self.create_session()
        if result is not None:
            if isinstance(result, Exception):
                raise result
            raise RuntimeError('Session creation failed: ' + str(result))
        return

    def execute(self) -> None:

        assert self.session is not None

        try:
            entity = Entity.create(
                self.session,
                'Test Entity',
                None,
                None
            )
        except Exception as error:
            self.record_failure(error)
            return

        self.entity = entity

        try:
            entity = Entity.retrieve(
                self.session,
                entity.id_
            )
        except Exception as error:
            self.record_failure(error)
            return

        if entity.id_ != self.entity.id_:
            self.record_failure('Entity ids do not match')
            return

        #new_name = 'Updated Entity Name'

        #try:
        #    entity.update(
        #        new_name,
        #        entity.description,
        #        entity.owner_id,
        #        entity.permissions_graph
        #    )
        #except Exception as error:
        #    self.record_failure(error)
        #    return

        #if entity.name != new_name:
        #    self.record_failure('Entity name not updated: ' + str(entity.name))
        #    return

        self.record_success()
        return
