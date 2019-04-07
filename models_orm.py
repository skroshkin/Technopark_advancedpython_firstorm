from fields_orm import Field, IntField, StringField


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')
        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name is empty')

        # todo mro

        fields = {k: v for k, v in namespace.items()
                  if isinstance(v, Field)}
        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        return self

    def create(self):
        print(self.model_cls)


class Model(metaclass=ModelMeta):
    class Meta:
        table_name = ''

    objects = Manage()

    # todo DoesNotExist

    def __init__(self, *_, **kwargs):
        for field_name, field in self.fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)


class User(Model):
    id = IntField()
    name = StringField()

    class Meta:
        table_name = ''


class Man(User):
    sex = StringField()


user = User(id=1, name='name')
User.objects.create(id=1, name='name')
User.objects.update(id=1)
User.objects.delete(id=1)

User.objects.filter(id=2).filter(name='petya')

user.name = '2'
user.save()
user.delete()
