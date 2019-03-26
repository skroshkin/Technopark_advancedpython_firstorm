from datetime import datetime


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        # todo exceptions
        return self.f_type(value)


class IntField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(int, required, default)

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError('only 0-9 numbers allowed')
        else:
            pass


class FloatField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(float, required, default)

    def validate(self, value):
        if not isinstance(value, float):
            raise TypeError('only float characters allowed')
        else:
            pass


class StringField(Field):
    def __init__(self, length=50, required=True, default=None):
        super().__init__(str, required, default)
        self.length = length

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError('only str type allowed')
        else:
            pass
        if len(value) > self.length:
            raise ValueError('only {} characters allowed'.format(self.length))
        else:
            pass


class TextField(StringField):
    def __init__(self, required=True, default=None):
        super().__init__(500, required, default)


class VarcharField(StringField):
    def __init__(self, required=True, default=None):
        super().__init__(50, required, default)


class DateField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(str, required, default)

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError('only str type allowed')
        else:
            pass
        if value != datetime.strptime(value, '%d.%m.%Y'):
            raise ValueError('only DD.MM.YYYY format allowed')
        else:
            pass
