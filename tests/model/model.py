from typed_models import Model
from typed_models import Field


class SampleModel(Model):
    test_field_1 = Field(default="Hello")
    test_field_2 = Field()
    test_field_3 = Field(optional=True)
    test_field_4 = Field(default="World", optional=True)
