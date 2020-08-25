from ..base import Field

class FloatField(Field):

    def parse(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            self._raise_value_error(value)

    def default_serializer(self, value):
        return value