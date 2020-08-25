from enum import Enum

from ..exceptions import InvalidFieldArguments
from ..base import Field, NOT_PROVIDED


class EnumField(Field):

    def __init__(self, enum_type=NOT_PROVIDED, default=NOT_PROVIDED, optional=False):
        super().__init__(default, optional)

        if enum_type is NOT_PROVIDED:
            raise InvalidFieldArguments('An EnumField requires a enum_type to be specified')

        if not issubclass(enum_type, Enum):
            raise TypeError(
                f'The enum_type specified must inherit from Enum. You have provided enum_type of type {type(enum_type)}')

        self.enum_type = enum_type

    def parse(self, value):
        try:
            return self.enum_type(value)  # noqa
        except ValueError as e:
            raise ValueError(
                f'Field "{self.field_name}" with value "{value}" could not be parsed as a {self.enum_type.__name__}') from None

    def default_serializer(self, value):
        return value.value
