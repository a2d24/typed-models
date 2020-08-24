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

    @classmethod
    def is_field(cls, value):
        return isinstance(value, cls)


class FieldValue:

    def __init__(self, field: Field, value=NOT_PROVIDED):
        self.field = field
        self.value = value

    def get(self):
        if self.value is NOT_PROVIDED:
            return self.field.get_default()

        return self.field.get(self.value)

    def set(self, value):
        self.value = self.field.set(value)


class ModelMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__

        module = attrs.pop('__module__')
        base_attrs = {'__module__': module}

        fields = {}
        field_names = []
        for field_name, value in list(attrs.items()):
            if Field.is_field(value):
                fields[field_name] = value
                field_names.append(field_name)
            else:
                base_attrs[field_name] = value

        new_class = super_new(cls, name, bases, base_attrs, **kwargs)

        # for field_name, field_value in fields.items():
        #     setattr(new_class, field_name, field_value)
        #
        # new_class._meta = {'field_names': field_names}
        # new_class._meta['fields'] = {name: fields[name] for name in field_names}
        new_class._model_meta = {
            'fields': fields,
            'field_names': field_names,
            'field_values': {}
        }
        return new_class


class Model(metaclass=ModelMeta):

    def __init__(self, **kwargs):
        source = {**kwargs}
        for field_name in self._model_meta['field_names']:
            field = self._model_meta['fields'][field_name]
            field_value = FieldValue(field=field)
            try:
                value = source.pop(field_name)
                field_value.set(value)
            except KeyError:
                pass

            self._model_meta['field_values'][field_name] = field_value
