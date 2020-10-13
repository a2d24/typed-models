from typed_models import Model, Field
from typed_models.fields import StringField, ListField, ModelField, BooleanField
from typed_models.base import NOT_PROVIDED

class CustomField(StringField):

    def serialize(self, value, serializer=NOT_PROVIDED):
        return f"{value}-CUSTOM"

class SampleModel(Model):
    test_field_1 = Field(default="Hello")
    test_field_2 = Field()
    test_field_3 = Field(optional=True)


class SampleModelWithCustomField(Model):
    custom_field = CustomField(optional=True)


class Contact(Model):
    name = StringField()
    number = StringField()

class Person(Model):
    first_name = StringField()
    last_name = StringField()
    contacts = ListField(list_type=ModelField(model_class=Contact))


class AwesomePerson(Person):
    is_awesome = BooleanField(default=True)

class SimpleList(Model):
    list = ListField(list_type=StringField())