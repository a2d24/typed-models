from ..base import Field

class StringField(Field):

    def set(self, value):
        return str(value)