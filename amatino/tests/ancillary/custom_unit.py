"""
Amatino API Python Bindings
Custom Unit Test Module
Author: hugh@amatino.io
"""
from amatino.tests.primary.entity import EntityTest
from amatino import CustomUnit


class CustomUnitTest(EntityTest):
    """Test the Custom Unit object"""

    def __init__(self, name='Create, retrieve, update a Custom Unit') -> None:

        super().__init__(name)
        self.create_entity()
        return

    def execute(self) -> None:

        try:
            custom_unit = CustomUnit.create(
                self.entity,
                'Bojangles',
                'BTX',
                4
            )
        except Exception as error:
            self.record_failure(error)
            return

        if not isinstance(custom_unit, CustomUnit):
            return_type = str(type(custom_unit))
            self.record_failure('Unexpected return type: ' + return_type)
            return

        if not isinstance(custom_unit.id_, int):
            id_type = str(type(custom_unit.id_))
            self.record_failure('Unexpected id type: ' + id_type)
            return

        if not isinstance(custom_unit.code, str):
            code_type = str(type(custom_unit.code))
            self.record_failure('Unexpected code type: ' + code_type)
            return

        try:
            retrieved_custom_unit = CustomUnit.retrieve(
                self.entity,
                custom_unit.id_
            )
        except Exception as error:
            self.record_failure(error)
            return

        if retrieved_custom_unit.id_ != custom_unit.id_:
            self.record_failure('Retrieved ID does not match')
            return

        new_name = 'CryptoJuice'

        try:
            updated_custom_unit = custom_unit.update(name=new_name)
        except Exception as error:
            self.record_failure(error)
            return

        if updated_custom_unit.name != new_name:
            self.record_failure('Name failed to update')
            return

        self.record_success()
        return
