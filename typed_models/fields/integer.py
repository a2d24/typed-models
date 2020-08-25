from ..base import Field

class IntegerField(Field):

    def parse(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            self._raise_value_error(value)

    def default_serializer(self, value):
        return value