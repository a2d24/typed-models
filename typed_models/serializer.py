from .exceptions import UnassignedOptionalFieldRequested


class DefaultSerializer:

    @staticmethod
    def serialize(model):

        output = {}

        for field_name, field_value in model._model_meta['field_values'].items():
            try:
                output[field_name] = DefaultSerializer.serialize_field(field_value)
            except UnassignedOptionalFieldRequested:
                pass

        return output

    @staticmethod
    def serialize_field(field_value):
        return field_value.field.default_serializer(field_value.get())
