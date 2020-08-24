import pytest

from typed_models.exceptions import DefaultNotProvided
from typed_models import FieldValue

from .model import SampleModel


@pytest.mark.parametrize('field_name', ['test_field_1', 'test_field_2', 'test_field_3', 'test_field_4'])
def test_all_fields_converted_to_field_values(field_name):
    sample = SampleModel()
    assert isinstance(sample._model_meta['field_values'][field_name], FieldValue)


def test_fields_initilized_with_defaults():
    sample = SampleModel()
    assert sample._model_meta['field_values']['test_field_1'].get() == 'Hello'
    assert sample._model_meta['field_values']['test_field_4'].get() == 'World'

def test_fields_initilized_with_kwargs():
    sample = SampleModel(test_field_1="test_1", test_field_3="test_3")
    assert sample._model_meta['field_values']['test_field_1'].get() == 'test_1'
    assert sample._model_meta['field_values']['test_field_3'].get() == 'test_3'

#
# def test_not_providing_required_field():
#     with pytest.raises(DefaultNotProvided):
#         SampleModel()
