from decimal import Decimal

from ..base import Field

class DecimalField(Field):

    def parse(self, value):
        if isinstance(value, Decimal):
            return value

        try:
            return Decimal(str(value))
        except Exception:
            self._raise_value_error(value)