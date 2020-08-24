import pytest

from .model import TestModelMeta
from typed_models import Field


def test_model_meta_copies_module():
    assert TestModelMeta.__module__ == 'tests.model_meta.model'


def test_non_field_attributes_are_copied():
    assert TestModelMeta.TEST_ATTRIBUTE == "Hello"


def test_field_attribute_not_copied():
    with pytest.raises(AttributeError):
        TestModelMeta.test_field  # noqa


def test_field_attributes_added_to_field_names():
    assert TestModelMeta._model_meta['field_names'] == ['test_field']


def test_field_attributes_added_to_metadata():
    assert list(TestModelMeta._model_meta['fields'].keys()) == ['test_field']
    assert isinstance(TestModelMeta._model_meta['fields']['test_field'], Field)