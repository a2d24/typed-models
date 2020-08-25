import pytest
from typed_models.fields import BooleanField


@pytest.mark.parametrize('input, expected_output', [
    (True, True), ('True', True), ('true', True),
    (False, False), ('False', False), ('false', False)
])
def test_setters(input, expected_output):
    field = BooleanField()
    assert field.set(input) == expected_output

def test_unparsable_raises_exception():
    field = BooleanField()

    with pytest.raises(ValueError):
        field.set('1')

def test_serializer():
    field = BooleanField()
    assert field.serialize(True) == True
    assert field.serialize(False) == False