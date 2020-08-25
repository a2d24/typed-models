import pytest
from typed_models.fields import IntegerField


@pytest.mark.parametrize('input, expected_output', [
    (1, 1), ('1', 1), (1.5, 1), (0, 0), (-1, -1), ('-1', -1), (-1.5, -1)
])
def test_setters(input, expected_output):
    field = IntegerField()
    assert field.set(input) == expected_output


def test_unparsable_raises_exception():
    field = IntegerField()

    with pytest.raises(ValueError):
        field.set('1.5')

    with pytest.raises(ValueError):
        field.set('hello')


def test_serializer():
    field = IntegerField()
    assert field.serialize(1) == 1
    assert field.serialize(-1) == -1
