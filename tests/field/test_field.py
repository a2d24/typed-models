from decimal import Decimal

import pytest

from typed_models import Field
from typed_models.exceptions import DefaultNotProvided, InvalidFieldArguments
from typed_models.base import NOT_PROVIDED

def test_init():
    field = Field()
    assert isinstance(field, Field)


def test_cannot_be_optional_and_have_default():
    with pytest.raises(InvalidFieldArguments):
        field = Field(optional=True, default="test")

def test_default_not_provided():
    field = Field()
    with pytest.raises(DefaultNotProvided):
        assert field.get_default() == NOT_PROVIDED


def test_default_provided():
    field = Field(default="test")
    assert field.get_default() == "test"


def test_optional_default_not_provided():
    field = Field(optional=True)
    assert field.get_default() == NOT_PROVIDED


def test_default_getter():
    field = Field()
    assert field.get("test") == "test"


def test_default_setter():
    field = Field()
    assert field.set("test") == "test"


@pytest.mark.parametrize(
    "input, expected", [
        (1, "1"),
        ("hello", "hello"),
        (True, "True"),
        (None, "None"),
        (5.5, "5.5"),
        (Decimal(5.5), "5.5"),
        (-1.5, "-1.5")
    ]
)
def test_default_serializer(input, expected):
    field = Field()
    assert field.serialize(input) == expected
