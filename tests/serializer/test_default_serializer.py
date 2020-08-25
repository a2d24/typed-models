from typed_models.serializer import DefaultSerializer

from ..model.model import SampleModel


def test_returns_strings():
    sample = SampleModel(test_field_2=1, test_field_3=True)

    assert DefaultSerializer.serialize(sample) == {
        'test_field_1': "Hello",
        'test_field_2': "1",
        'test_field_3': "True",
    }


def test_does_not_return_unassigned_optional_fields():
    sample = SampleModel(test_field_2=None)

    assert DefaultSerializer.serialize(sample) == {
        'test_field_1': "Hello",
        'test_field_2': "None",
    }


def test_returns_assigned_optional_fields():
    sample = SampleModel(test_field_2=None, test_field_3="Hi")

    assert DefaultSerializer.serialize(sample) == {
        'test_field_1': "Hello",
        'test_field_2': "None",
        'test_field_3': "Hi"
    }
