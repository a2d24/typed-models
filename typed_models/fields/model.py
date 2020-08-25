from ..exceptions import InvalidFieldArguments
from ..base import Field, Model, NOT_PROVIDED


class ModelField(Field):

    def __init__(self, model_class=NOT_PROVIDED, default=NOT_PROVIDED, optional=False):
        super().__init__(default, optional)

        if model_class is NOT_PROVIDED:
            raise InvalidFieldArguments('A ModelField requires a model_class to be specified')

        if not issubclass(model_class, Model):
            raise TypeError(
                f'The ModelClass specified must inherit from Model. You have provided model_class of type {type(model_class)}')

        self.ModelClass = model_class

    def parse(self, value):
        if isinstance(value, dict):
            return self.ModelClass(value)

        if not isinstance(value, self.ModelClass):
            self._raise_value_error(value)

        return value


    def serialize(self, value, serializer=NOT_PROVIDED):
        if serializer is NOT_PROVIDED:
            raise RuntimeError("A serializer is expected to serialize a Model")

        return serializer.serialize(value)