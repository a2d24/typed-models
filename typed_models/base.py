from .exceptions import DefaultNotProvided

NOT_PROVIDED = object()


class Field:

    def __init__(self, default=NOT_PROVIDED, optional=False):
        self.default = default
        self.optional = optional
        self.field_name = 'Field'

    def get_default(self):

        if self.default is not NOT_PROVIDED:
            return self.default

        if self.optional:
            return NOT_PROVIDED

        raise DefaultNotProvided(f"Field '{self.field_name}' has no default specified and is not optional")

    def get(self, value):
        return value

    def set(self, value):
        return value

    def serialize(self, value):
        return str(value)


class FieldInstance:

    def __init__(self, field, value=NOT_PROVIDED):
        self.field = field
        self.value = value

    def get(self):
        if self.value is NOT_PROVIDED:
            return self.field.get_default()

        return self.field.get(self.value)


class Model:
    pass
