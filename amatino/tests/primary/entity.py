"""
Amatino API Python Bindings
Entity Test Module
Author: hugh@amatino.io
"""
from amatino.entity import Entity
from amatino.tests.ancillary.session import SessionTest
from amatino import Session


class EntityTest(SessionTest):
    """
    Test the Entity primary object
    """

    def __init__(self, name='Create, retrieve, update an Entity') -> None:

        self.entity = None

        super().__init__(name)
        self.create_session()
        if not isinstance(self.session, Session):
            raise RuntimeError(
                'Session creation failed, consider running Session tests'
            )
        return

    def create_entity(self) -> Entity:
        entity = Entity.create(
            self.session,
            'Test Entity',
            None,
            None
        )
        self.entity = entity
        return entity

    def execute(self) -> None:

        assert self.session is not None

        try:
            entity = self.create_entity()
        except Exception as error:
            self.record_failure(error)
            return

        assert isinstance(self.entity, Entity)

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

        new_name = 'Updated Entity Name'

        try:
            updated_entity = entity.update(new_name)
        except Exception as error:
            self.record_failure(error)
            return

        if updated_entity.name != new_name:
            self.record_failure('Entity name not updated: ' + str(entity.name))
            return

        listed_entities = Entity.retrieve_list(
            session=self.session
        )

        assert isinstance(listed_entities, list)
        assert len(listed_entities) > 0

        self.record_success()
        return
