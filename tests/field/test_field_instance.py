import pytest
from typed_models import Field, FieldInstance
from typed_models.exceptions import DefaultNotProvided
from typed_models.base import NOT_PROVIDED

def test_field_instance_init():
    field = Field()
    field_instance = FieldInstance(field=field)

    assert isinstance(field_instance, FieldInstance)
    assert field_instance.field == field

def test_field_instance_no_default_value():
    field_instance = FieldInstance(field=Field())

    with pytest.raises(DefaultNotProvided):
        field_instance.get()

def test_field_instance_default_value():
    field_instance = FieldInstance(field=Field(default="hello"))
    assert field_instance.get() == "hello"