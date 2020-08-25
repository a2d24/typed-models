import pytest

from typed_models.exceptions import DefaultNotProvided, UnassignedOptionalFieldRequested
from typed_models import FieldValue

from .model import SampleModel, Contact, Person


@pytest.mark.parametrize('field_name', ['test_field_1', 'test_field_2', 'test_field_3'])
def test_all_fields_converted_to_field_values(field_name):
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert isinstance(sample._field_values[field_name], FieldValue)


def test_fields_initialized_with_defaults():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert sample._field_values['test_field_1'].get() == 'Hello'


def test_fields_initialized_with_kwargs():
    sample = SampleModel(test_field_1="test_1", test_field_3="test_3", test_field_2="Required Feild Dummy Value")
    assert sample._field_values['test_field_1'].get() == 'test_1'
    assert sample._field_values['test_field_3'].get() == 'test_3'


def test_fields_initialized_with_dict():
    sample = SampleModel({
        "test_field_1": "test_1",
        "test_field_2": "test_2",
        "test_field_3": "test_3"
    })
    assert sample._field_values['test_field_1'].get() == 'test_1'
    assert sample._field_values['test_field_3'].get() == 'test_3'


def test_kwargs_higher_priority_than_dict():
    sample = SampleModel({
        "test_field_1": "test_1",
        "test_field_2": "test_2",
        "test_field_3": "test_3"
    }, test_field_1="hello", test_field_3="world")
    assert sample._field_values['test_field_1'].get() == 'hello'
    assert sample._field_values['test_field_3'].get() == 'world'


def test_missing_required_field_throws():
    with pytest.raises(DefaultNotProvided):
        sample = SampleModel()


def test_access_using_attributes():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    assert sample.test_field_1 == 'Hello'


def test_access_of_unset_optional_field_throws():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    with pytest.raises(UnassignedOptionalFieldRequested):
        sample.test_field_3  # noqa


def test_setting_of_attribute_sets_field_value():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    sample.test_field_2 = "Hello, World"

    assert sample.test_field_2 == "Hello, World"


def test_can_set_non_field_attributes():
    sample = SampleModel(test_field_2="Required Field Dummy Value")
    sample.test_attribute = "Hello"
    assert sample.test_attribute == "Hello"


def test_each_model_fields_values_are_unique_instances():
    sample_1 = SampleModel(test_field_2="Instance 1")
    sample_2 = SampleModel(test_field_2="Instance 2")

    assert sample_1.test_field_2 == "Instance 1"
    assert sample_2.test_field_2 == "Instance 2"


def test_can_serialize_models():
    person = Person({'first_name': 'John', 'last_name': 'Doe', 'contacts': [{
        "name": "Mary", "number": "+2782911"
    }]})
    person.contacts.append(Contact(name='Jane', number='082'))
    person.contacts.append(Contact(name='James', number='911'))

    assert person.serialize() == {
        "first_name": "John",
        "last_name": "Doe",
        "contacts": [
            {
                "name": "Mary",
                "number": "+2782911"
            },
            {
                "name": "Jane",
                "number": "082"
            },
            {
                "name": "James",
                "number": "911"
            }
        ]
    }
