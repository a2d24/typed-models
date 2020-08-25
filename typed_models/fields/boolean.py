from ..base import Field

class BooleanField(Field):

    def parse(self, value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            if value.lower() in ['true', 'True']:
                return True
            elif value.lower() in ['false', 'False']:
                return False

        self._raise_value_error(value)

    def default_serializer(self, value):
        return value