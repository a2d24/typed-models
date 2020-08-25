from decimal import Decimal

import pytest

from typed_models.fields import DecimalField


@pytest.mark.parametrize('input, expected_output', [
    (1, Decimal(1)),
    ('1.0', Decimal('1.0')),
    (0.33, Decimal('0.33')),
    (-1.33, Decimal('-1.33')),
    (5 - 2, Decimal('3')),
    (Decimal('1'), Decimal('1'))
])
def test_setters(input, expected_output):
    field = DecimalField()
    parsed = field.parse(input)
    assert parsed == expected_output
    assert isinstance(parsed, Decimal)


def test_unparsable_raises_exception():
    field = DecimalField()

    with pytest.raises(ValueError):
        field.parse(None)

    with pytest.raises(ValueError):
        field.parse('hello')


def test_serializer():
    field = DecimalField()
    assert field.default_serializer(1) == "1"
    assert field.default_serializer(-1) == "-1"
    assert field.default_serializer(-1.0) == "-1.0"
