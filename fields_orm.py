from datetime import datetime
import re

vulnerabilities_keywords = [
    'select', 'union', 'insert', 'update', 'drop',
    'alter', '--', 'or', 'and'
]

Type_Error = 'only {} type allowed'


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        if re.match(r'\s', value):
            raise ValueError('space at the beginning of the field is not allowed')
        if not isinstance(value, str):
            raise Type_Error.format(str)
        # я понимаю, что сочетание букв or и and могут встречаться в обычных словах
        for key_word in vulnerabilities_keywords:
            if value.lower().find(key_word.lower()) != -1:
                print('Warning: this string has vulnerabilities')
                break
        return self.f_type(value)


class IntField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(int, required, default)

    def validate(self, value):
        if not isinstance(value, int):
            raise Type_Error.format('int')


class FloatField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(float, required, default)

    def validate(self, value):
        if not isinstance(value, float):
            raise Type_Error.format('float')


class StringField(Field):
    def __init__(self, length=50, required=True, default=None):
        super().__init__(str, required, default)
        self.length = length

    def validate(self, value):
        if not isinstance(value, str):
            raise Type_Error.format('str')
        if len(value) > self.length:
            raise ValueError('only {} characters allowed'.format(self.length))


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
            raise Type_Error.format('str')
        if value != datetime.strptime(value, '%d.%m.%Y'):
            raise ValueError('only DD.MM.YYYY format allowed')
