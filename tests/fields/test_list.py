import pytest
import pendulum

from typed_models.exceptions import InvalidFieldArguments
from typed_models.fields import ListField, DateTimeField, StringField
from typed_models.base import FieldValue
from typed_models.fields.list import TypedFieldList


class CustomSerializer:
    @staticmethod
    def serialize_field(f):
        return str(f.get()) + '+CUSTOM'


def test_init_requires_list_type():
    with pytest.raises(InvalidFieldArguments):
        field = ListField()

    with pytest.raises(TypeError):
        field = ListField(list_type=float)

    field = ListField(list_type=DateTimeField())


def test_inits_with_empty_list():
    field = ListField(list_type=DateTimeField())
    assert field.get_default().list == []


def test_only_accepts_lists():
    field = ListField(list_type=DateTimeField())
    with pytest.raises(TypeError):
        field.parse('Hello')


def test_strongly_typed_list():
    field = ListField(list_type=DateTimeField(tz='UTC'))

    with pytest.raises(ValueError):
        field.parse(['hello'])

    now = pendulum.now(tz='Africa/Johannesburg')
    now_in_utc = now.in_tz('UTC')
    result = field.parse(['2020-01-01', '2020-01-02T22:10+0200', now])

    assert_datetime(result[0], 2020, 1, 1)
    assert_datetime(result[1], 2020, 1, 2, hour=20, minute=10)
    assert_datetime(result[2],
                    now_in_utc.year,
                    now_in_utc.month,
                    now_in_utc.day,
                    hour=now_in_utc.hour,
                    minute=now_in_utc.minute,
                    second=now_in_utc.second,
                    microsecond=now_in_utc.microsecond
                    )


def test_can_append_with_strong_typing_to_empty_list():
    field = ListField(list_type=DateTimeField(tz='UTC'))
    value = FieldValue(field=field)
    typed_list = value.get()

    with pytest.raises(ValueError):
        typed_list.append('Hello')

    typed_list.append('2020-01-01')
    typed_list.append('2020-01-02')

def test_list_get_accessor_returns_list_of_internal_values():
    field = ListField(list_type=StringField())
    value = FieldValue(field=field)
    value.set(["Hello", "World"])

    assert list(value.get()) == ["Hello", "World"]

def test_serializer():
    field = ListField(list_type=DateTimeField(tz='UTC'))
    result = field.parse(['2020-01-01', '2020-01-02T22:10+0200'])
    serialized = field.serialize(result)
    assert serialized == ['2020-01-01T00:00:00+00:00', '2020-01-02T20:10:00+00:00']


def test_custom_serializer():
    field = ListField(list_type=DateTimeField(tz='UTC'))

    result = field.parse(['2020-01-01', '2020-01-02T22:10+0200'])

    serialized = field.serialize(result, serializer=CustomSerializer)
    assert serialized == ['2020-01-01T00:00:00+00:00+CUSTOM', '2020-01-02T20:10:00+00:00+CUSTOM']


def test_can_parse_typed_field_list():
    list_type = DateTimeField(tz='UTC')
    field = ListField(list_type=list_type)
    typed_field_list = TypedFieldList(field_type=list_type)
    assert len(field.parse(typed_field_list)) == 0


def test_can_delete_item():
    field = ListField(list_type=StringField())
    list = field.parse([])

    list.append("Hello")
    list.append("World")
    list.append("Test")

    del list[2]

    assert [l for l in list] == ['Hello', 'World']

def test_can_replace_item():
    field = ListField(list_type=StringField())
    l = field.parse(['Hello', 'Wrong'])
    l[1] = 'World'
    assert list(l) == ['Hello', 'World']

def test_list_str_representation():
    field = ListField(list_type=StringField())
    list = field.parse(['Hello', 'World'])
    assert str(list) == "['Hello', 'World']"


def assert_datetime(
        d, year, month, day, hour=None, minute=None, second=None, microsecond=None
):
    assert year == d.year
    assert month == d.month
    assert day == d.day

    if hour is not None:
        assert hour == d.hour

    if minute is not None:
        assert minute == d.minute

    if second is not None:
        assert second == d.second

    if microsecond is not None:
        assert microsecond == d.microsecond
