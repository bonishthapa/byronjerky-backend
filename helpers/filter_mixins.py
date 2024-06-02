from datetime import datetime

from django.contrib import admin
from django.db import models

from django_filters.filters import ModelChoiceFilter
from django_filters.filterset import (
    FILTER_FOR_DBFIELD_DEFAULTS,
    FilterSet,
    remote_queryset,
)
from django_filters.rest_framework import DjangoFilterBackend

FILTER_FOR_DBFIELD_DEFAULTS[models.OneToOneField] = {
    "filter_class": ModelChoiceFilter,
    "extra": lambda f: {
        "queryset": remote_queryset(f),
        "to_field_name": "idx",
    },
}

FILTER_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {
    "filter_class": ModelChoiceFilter,
    "extra": lambda f: {
        "queryset": remote_queryset(f),
        "to_field_name": "idx",
    },
}


class BaseFilterSet(FilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS


class BaseDjangoFilterBackend(DjangoFilterBackend):
    filterset_base = BaseFilterSet


def filter_boolean(queryset, name, value):
    m = {"true": True, "false": False}
    kwargs = {name: m.get(value)}
    return queryset.filter(**kwargs)


def filter_multiple(queryset, name, value):
    kwargs = {f"{name}__in": value.split(",")}
    return queryset.filter(**kwargs)


class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice["query_parts"] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class StartDateFilter(InputFilter):
    parameter_name = "created_on_np_date__gte"
    title = "Start Date"

    def queryset(self, request, queryset):
        if self.value():
            try:
                start_date = datetime.strptime(self.value(), "%Y-%m-%d").date()
            except ValueError:
                return queryset.none()
            return queryset.filter(created_on_np_date__gte=start_date)


class EndDateFilter(InputFilter):
    parameter_name = "created_on_np_date__lte"
    title = "End Date"

    def queryset(self, request, queryset):
        if self.value():
            try:
                end_date = datetime.strptime(self.value(), "%Y-%m-%d").date()
            except ValueError:
                return queryset.none()
            return queryset.filter(created_on_np_date__lte=end_date)


class DateFilter(InputFilter):
    parameter_name = "created_on_np_date"
    title = "Created on"

    def queryset(self, request, queryset):
        if self.value():
            try:
                date = datetime.strptime(self.value(), "%Y-%m-%d").date()
            except ValueError:
                return queryset.none()
            return queryset.filter(created_on_np_date=date)
