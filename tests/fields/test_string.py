import pytest
from typed_models.fields import StringField


@pytest.mark.parametrize('input, expected_output', [
    (True, "True"), ('hello', 'hello'), (None, 'None'), (1, "1"), (1.25, "1.25")
])
def test_setters(input, expected_output):
    field = StringField()
    assert field.parse(input) == expected_output