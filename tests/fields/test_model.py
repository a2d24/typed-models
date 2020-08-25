import pytest

from typed_models.exceptions import InvalidFieldArguments
from typed_models.serializer import DefaultSerializer
from typed_models.fields import ModelField
from typed_models import Model, Field


class SimpleModel(Model):
    simple_field = Field(default='Hello')

class NestedModel(Model):
    nested_field = ModelField(model_class=SimpleModel)

def test_init_requires_model():
    with pytest.raises(InvalidFieldArguments):
        field = ModelField()

    with pytest.raises(TypeError):
        field = ModelField(model_class=float)

    field = ModelField(model_class=SimpleModel)


def test_parse_from_model():
    field = ModelField(model_class=SimpleModel)

    parsed = field.parse(SimpleModel(simple_field='Hello'))
    assert parsed.simple_field == 'Hello'


def test_parse_from_dict():
    field = ModelField(model_class=SimpleModel)

    parsed = field.parse(dict(simple_field='Hello'))

    assert parsed.simple_field == 'Hello'


def test_unparsable_raises_exception():
    field = ModelField(model_class=SimpleModel)

    with pytest.raises(ValueError):
        field.parse(None)

    with pytest.raises(ValueError):
        field.parse('Hello, World')


def test_using_default_serializer():
    model = NestedModel(nested_field=SimpleModel(simple_field="Hello, World!"))
    serialized = DefaultSerializer.serialize(model)

    assert serialized == {
        'nested_field': {'simple_field': "Hello, World!"}
    }


def test_no_serializer_provided():
    field = ModelField(model_class=SimpleModel)

    value = field.parse({})
    with pytest.raises(RuntimeError):
        field.serialize(value)