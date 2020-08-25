from ..base import Field

class IntegerField(Field):

    def set(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            self._raise_value_error(value)

    def serialize(self, value):
        return value