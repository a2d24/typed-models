import pytest
from typed_models import Field, FieldValue
from typed_models.exceptions import DefaultNotProvided


def test_init():
    field = Field()
    field_instance = FieldValue(field=field)

    assert isinstance(field_instance, FieldValue)
    assert field_instance.field == field


def test_no_default_value():
    field_instance = FieldValue(field=Field())

    with pytest.raises(DefaultNotProvided):
        field_instance.get()


def test_default_value():
    field_instance = FieldValue(field=Field(default="hello"))
    assert field_instance.get() == "hello"


def test_getter_and_setter():
    value = FieldValue(field=Field())
    value.set("hello")

    assert value.get() == "hello"
