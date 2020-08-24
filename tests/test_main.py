from typed_models import Model, Field


def test_model():
    assert isinstance(Model(), Model)


def test_field():
    assert isinstance(Field(), Field)
