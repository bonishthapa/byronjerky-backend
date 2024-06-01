from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import serializers
from rest_framework.fields import get_attribute, is_simple_callable

from helpers.exceptions import BaseException


class TzDateTimeField(serializers.DateTimeField):
    """
    Timezone aware DateTimeField for DRF.
    """

    def to_representation(self, obj):
        obj = obj.astimezone(timezone.get_current_timezone())
        date = super().to_representation(obj)
        return date


class DetailRelatedField(serializers.RelatedField):
    """
    Read/write serializer field for relational field.
    Syntax:
            DetailRelatedField(Model, [lookup], representation)

            Model: model to which the serializer field is related to
            lookup: field for getting a model instance, if not supplied it defaults to idx
            representation: a model instance method name for getting serialized data
    """

    def __init__(self, model, **kwargs):
        if not kwargs.get("read_only"):
            kwargs["queryset"] = model.objects.all()

        self.lookup = kwargs.pop("lookup", None) or "idx"

        try:
            self.representation = kwargs.pop("representation")
        except KeyError:
            raise BaseException("Please supply representation.")

        super(DetailRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.queryset.get(**{self.lookup: data})
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist.")

    def to_representation(self, obj):
        return getattr(obj, self.representation)()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        # cast representation of item to str because
        # to representation could return a dict
        # and dicts can't be used as key on dicts because dicts are not hashable
        return {
            str(self.to_representation(item)): self.display_value(item)
            for item in queryset
        }


class IDXOnlyObject:
    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return "%s" % self.idx


class BaseRelatedField(serializers.PrimaryKeyRelatedField):
    default_error_messages = {
        "required": "This field is required.",
        "does_not_exist": 'Invalid idx "{pk_value}" - object does not exist.',
        "incorrect_type": "Incorrect type. Expected idx value, received {data_type}.",
    }

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            # Optimized case, return a mock object only containing the pk attribute.
            try:
                instance = get_attribute(instance, self.source_attrs[:-1])
                value = instance.serializable_value(self.source_attrs[-1])
                if is_simple_callable(value):
                    # Handle edge case where the relationship `source` argument
                    # points to a `get_relationship()` method on the model
                    value = value().idx
                else:
                    value = getattr(instance, self.source_attrs[-1]).idx
                return IDXOnlyObject(idx=value)
            except AttributeError:
                pass

    def to_representation(self, obj):
        return obj.idx

    def to_internal_value(self, data):
        try:
            return self.queryset.get(idx=data)
        except ObjectDoesNotExist:
            self.fail("does_not_exist", pk_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)
