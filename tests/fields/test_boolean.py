import pytest
from typed_models.fields import BooleanField


@pytest.mark.parametrize('input, expected_output', [
    (True, True), ('True', True), ('true', True),
    (False, False), ('False', False), ('false', False)
])
def test_setters(input, expected_output):
    field = BooleanField()
    assert field.parse(input) == expected_output

def test_unparsable_raises_exception():
    field = BooleanField()

    with pytest.raises(ValueError):
        field.parse('1')

def test_serializer():
    field = BooleanField()
    assert field.default_serializer(True) == True
    assert field.default_serializer(False) == False