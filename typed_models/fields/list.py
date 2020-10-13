from collections.abc import MutableSequence

from ..exceptions import InvalidFieldArguments
from ..base import Field, NOT_PROVIDED, FieldValue
from .model import ModelField


class ListField(Field):

    def __init__(self, list_type=NOT_PROVIDED, default=NOT_PROVIDED, optional=False):
        if list_type is NOT_PROVIDED:
            raise InvalidFieldArguments('An ListField requires a list_type to be specified')

        if not isinstance(list_type, Field):
            raise TypeError(
                f'The list_type specified must be an instance of a subclass of Field. You have provided list_type of type {type(list_type)}')

        self.ListType = list_type

        default_value = default if default is not NOT_PROVIDED else self.parse([])

        super().__init__(default_value, optional)

    def parse(self, value):
        if not isinstance(value, list) and not isinstance(value, TypedFieldList):
            raise TypeError(
                f'Field "{self.field_name}" expects a value of type list, however {type(value)} was provided')

        typed_field_list = TypedFieldList(self.ListType)
        typed_field_list.extend(value)
        return typed_field_list

    def serialize(self, value, serializer=NOT_PROVIDED):
        if serializer is NOT_PROVIDED:
            return [self.ListType.default_serializer(v) for v in value]

        if isinstance(self.ListType, ModelField):
            return [serializer.serialize(v) for v in value]

        raw_fields = [value.get_raw(i) for i in range(len(value))]
        return [serializer.serialize_field(v) for v in raw_fields]


class TypedFieldList(MutableSequence):

    def __init__(self, field_type, *args):
        self.field_type: Field = field_type
        self.list = list()
        self.extend(list(args))

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i].get()

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        field_value = FieldValue(field=self.field_type)
        field_value.set(v)
        self.list[i] = field_value

    def insert(self, i, v):
        field_value = FieldValue(field=self.field_type)
        field_value.set(v)

        self.list.insert(i, field_value)

    def get_raw(self, i):
        return self.list[i]

    def __str__(self):
        return str([str(i.get()) for i in self.list])
