from ..base import Field

class StringField(Field):

    def parse(self, value):
        return str(value)