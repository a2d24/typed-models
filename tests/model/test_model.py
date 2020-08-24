import pytest

from typed_models.exceptions import DefaultNotProvided, UnassignedOptionalFieldAccessed
from typed_models import FieldValue

from .model import SampleModel


@pytest.mark.parametrize('field_name', ['test_field_1', 'test_field_2', 'test_field_3', 'test_field_4'])
def test_all_fields_converted_to_field_values(field_name):
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert isinstance(sample._model_meta['field_values'][field_name], FieldValue)


def test_fields_initialized_with_defaults():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert sample._model_meta['field_values']['test_field_1'].get() == 'Hello'
    assert sample._model_meta['field_values']['test_field_4'].get() == 'World'


def test_fields_initialized_with_kwargs():
    sample = SampleModel(test_field_1="test_1", test_field_3="test_3", test_field_2="Required Feild Dummy Value")
    assert sample._model_meta['field_values']['test_field_1'].get() == 'test_1'
    assert sample._model_meta['field_values']['test_field_3'].get() == 'test_3'


def test_fields_initialized_with_dict():
    sample = SampleModel({
        "test_field_1": "test_1",
        "test_field_2": "test_2",
        "test_field_3": "test_3"
    })
    assert sample._model_meta['field_values']['test_field_1'].get() == 'test_1'
    assert sample._model_meta['field_values']['test_field_3'].get() == 'test_3'


def test_kwargs_higher_priority_than_dict():
    sample = SampleModel({
        "test_field_1": "test_1",
        "test_field_2": "test_2",
        "test_field_3": "test_3"
    }, test_field_1="hello", test_field_3="world")
    assert sample._model_meta['field_values']['test_field_1'].get() == 'hello'
    assert sample._model_meta['field_values']['test_field_3'].get() == 'world'


def test_missing_required_field_throws():
    with pytest.raises(DefaultNotProvided):
        sample = SampleModel()


def test_access_using_attributes():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert sample.test_field_1 == 'Hello'


def test_access_of_unset_optional_field_throws():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    with pytest.raises(UnassignedOptionalFieldAccessed):
        sample.test_field_3  # noqa

def test_setting_of_attribute_sets_field_value():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    sample.test_field_2 = "Hello, World"

    assert sample.test_field_2 == "Hello, World"

def test_can_set_non_field_attributes():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    sample.test_attribute = "Hello"
    assert sample.test_attribute == "Hello"