from typed_models import Model, Field

def test_model():
    model = Model()

    assert isinstance(model, Model)

def test_field():
    field = Field()

    assert isinstance(field, Field)