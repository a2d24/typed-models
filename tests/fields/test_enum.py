import pytest
import enum

from typed_models.exceptions import InvalidFieldArguments
from typed_models.fields import EnumField

class SampleEnum(enum.Enum):
    OPTION_1 = 'option_1'
    OPTION_2 = 'option_2'


def test_init_requires_enum():
    with pytest.raises(InvalidFieldArguments):
        enum_field = EnumField()

    with pytest.raises(TypeError):
        enum_field = EnumField(enum_type=float)

    enum_field = EnumField(enum_type=SampleEnum)

def test_parse():
    field = EnumField(enum_type=SampleEnum)

    assert field.parse('option_1') == SampleEnum.OPTION_1
    assert field.parse('option_2') == SampleEnum.OPTION_2
    assert field.parse(SampleEnum.OPTION_1) == SampleEnum.OPTION_1
    assert field.parse(SampleEnum.OPTION_2) == SampleEnum.OPTION_2


def test_unparsable_raises_exception():
    field = EnumField(enum_type=SampleEnum)

    with pytest.raises(ValueError):
        field.parse(None)

    with pytest.raises(ValueError):
        field.parse('option_3')



def test_serializer():
    field = EnumField(enum_type=SampleEnum)
    assert field.default_serializer(field.parse(SampleEnum.OPTION_1)) == "option_1"