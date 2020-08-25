import pytest
import pendulum

from typed_models.fields import DateTimeField


@pytest.mark.parametrize('input, expected_output', [
    (pendulum.today(), pendulum.today()),
    ('2020-01-01T00:00:00Z', pendulum.parse('2020-01-01T00:00:00Z')),
])
def test_setters(input, expected_output):
    field = DateTimeField()
    parsed = field.parse(input)
    assert parsed == expected_output
    assert isinstance(parsed, pendulum.DateTime)


@pytest.mark.parametrize('tz, input, expected_output', [
    ('UTC', '2020-01-01T02:00:00+0200', pendulum.parse('2020-01-01T00:00:00Z')),
    ('Africa/Johannesburg', '2020-01-01T02:00:00+0200', pendulum.parse('2020-01-01T02:00:00+0200')),
    ('Africa/Johannesburg', '2020-01-01T05:00:00+0500', pendulum.parse('2020-01-01T02:00:00+0200')),
])
def test_setters_tz(tz, input, expected_output):
    field = DateTimeField(tz=tz)
    parsed = field.parse(input)
    assert parsed == expected_output
    assert parsed.utcoffset() == expected_output.utcoffset()
    assert isinstance(parsed, pendulum.DateTime)



def test_unparsable_raises_exception():
    field = DateTimeField()

    with pytest.raises(ValueError):
        field.parse(None)

    with pytest.raises(ValueError):
        field.parse('2020-00-00T00:00:00Z')


def test_serializer():
    field = DateTimeField()
    assert field.default_serializer(field.parse("2020-01-01T05:00:00+0500")) == "2020-01-01T00:00:00+00:00"
    assert field.default_serializer(field.parse("2020-01-01T05:00:00")) == "2020-01-01T05:00:00+00:00"
    assert field.default_serializer(field.parse("2020-01-01")) == "2020-01-01T00:00:00+00:00"

def test_auto_now():
    field = DateTimeField(default=DateTimeField.AUTO_NOW)
    start_time = pendulum.now()
    auto_time = field.get_default()
    end_time = pendulum.now()

    assert start_time < auto_time
    assert end_time > auto_time

def test_defaut():
    field_1 = DateTimeField(default='2020-01-01T00:00:00Z')
    assert field_1.get_default() == pendulum.parse('2020-01-01T00:00:00Z')


def test_default_handles_timezone():
    current_time = pendulum.now(tz='UTC')
    field_2 = DateTimeField(default=current_time, tz='Africa/Johannesburg')
    assert field_2.get_default() == current_time
    assert field_2.get_default().tz.name == 'Africa/Johannesburg'