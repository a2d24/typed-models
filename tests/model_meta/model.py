from typed_models.base import ModelMeta
from typed_models import Field


class TestModelMeta(metaclass=ModelMeta):
    TEST_ATTRIBUTE = "Hello"
    test_field = Field(default="World")
