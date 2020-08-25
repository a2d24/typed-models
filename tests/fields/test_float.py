import pytest
from typed_models.fields import FloatField


@pytest.mark.parametrize('input, expected_output', [
    (1, 1.0), ('1', 1.0), (1.5, 1.5), (0, 0.0), (-1, -1.0), ('-1', -1.0), (-1.5, -1.5)
])
def test_setters(input, expected_output):
    field = FloatField()
    parsed = field.parse(input)
    assert parsed == expected_output
    assert isinstance(parsed, float)


def test_unparsable_raises_exception():
    field = FloatField()

    with pytest.raises(ValueError):
        field.parse(None)

    with pytest.raises(ValueError):
        field.parse('hello')


def test_serializer():
    field = FloatField()
    assert field.default_serializer(1) == 1.0
    assert field.default_serializer(-1) == -1.0
    assert isinstance(field.default_serializer(1.0), float)
    assert isinstance(field.default_serializer(-1.5), float)
