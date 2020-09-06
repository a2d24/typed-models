import pendulum

from ..base import Field, NOT_PROVIDED


class DateTimeField(Field):

    AUTO_NOW = 'AUTO_NOW'

    def __init__(self, default=NOT_PROVIDED, optional=False, tz='UTC'):
        super().__init__(default, optional)
        self.tz = tz

    def parse(self, value):
        if isinstance(value, pendulum.DateTime):
            return self._set_tz(value)

        try:
            return self._set_tz(pendulum.parse(value))
        except (pendulum.exceptions.ParserError, TypeError):
            self._raise_value_error(value)

    def _set_tz(self, dt):
        return dt.in_tz(tz=self.tz)

    def get_default(self):
        if self.default == self.AUTO_NOW:
            return self._set_tz(pendulum.now())

        default = super().get_default()
        if default is NOT_PROVIDED:
            return default

        return self.parse(default)