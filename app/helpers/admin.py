import csv

from django.contrib.admin import ModelAdmin
from django.core.paginator import Paginator
from django.db import models
from django.db.models import DateTimeField
from django.forms import SplitDateTimeWidget
from django.http import HttpResponse
from django.utils import timezone

from django_json_widget.widgets import JSONEditorWidget
from django_summernote.admin import SummernoteModelAdmin

from helpers.db_helpers import db_enable_long_query
from helpers.filter_mixins import DateFilter, EndDateFilter, StartDateFilter


def export_data(headers, data, filename):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.DictWriter(response, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    return response


class ExportCsvMixin:
    export_fields = []
    export_serializer = None

    def export_as_csv(self, request, queryset):
        db_enable_long_query(600000)
        meta = self.model._meta
        if self.export_serializer:
            data = self.export_serializer(queryset, many=True).data
            fields = self.export_serializer.Meta.fields
            response = export_data(fields, data, f"{meta}.csv")
            return response
        if not self.export_fields:
            field_names = [field.name for field in meta.fields]
        else:
            field_names = self.export_fields

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"


class NoCountPaginator(Paginator):
    @property
    def count(self):
        return 999999999  # Some arbitrarily large number, so we can still get our page tab.


class BaseModelAdmin(ModelAdmin):
    use_date_range = False
    show_date_filter = False
    possible_readonly_fields = ["created_on", "modified_on", "deleted_on"]
    possible_raw_id_fields = [
        "user",
    ]
    paginator = NoCountPaginator

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.raw_id_fields = self.get_raw_id_fields(model)

    def get_readonly_fields(self, request, obj):
        readonly_fields = list(self.readonly_fields)
        for x in filter(lambda x: hasattr(obj, x), self.possible_readonly_fields):
            readonly_fields.append(x)
        return list(set(readonly_fields))

    def get_raw_id_fields(self, model):
        raw_id_fields = list(self.raw_id_fields)
        for x in filter(lambda x: hasattr(model, x), self.possible_raw_id_fields):
            raw_id_fields.append(x)
        return list(set(raw_id_fields))

    def get_exclude(self, request, obj):
        return self.possible_readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            if hasattr(obj, "created_by_id") and obj.created_by_id is None:
                obj.created_by_id = request.user.id
            if hasattr(obj, "performed_by_id") and obj.performed_by_id is None:
                obj.performed_by_id = request.user.id

        if obj.is_deleted is True and any(
            [obj.deleted_on is None, obj.is_deleted == ""]
        ):
            obj.deleted_on = timezone.now()
        obj.save()

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        DateTimeField: {
            "widget": SplitDateTimeWidget(
                date_attrs={
                    "type": "date",
                    "class": "vDateField mr-2",
                },
                time_attrs={"type": "time", "class": "vTimeField"},
            )
        },
    }

    def get_list_filter(self, request):
        if self.show_date_filter:
            if self.use_date_range:
                filter_list = (StartDateFilter, EndDateFilter)
            else:
                filter_list = (DateFilter,)
        else:
            filter_list = ()
        return super(BaseModelAdmin, self).get_list_filter(request) + filter_list

    list_per_page = 50


class SummernoteBaseModelAdmin(SummernoteModelAdmin, BaseModelAdmin):
    pass


class CustomReadonlyAdmin(BaseModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class CustomCreateOnlyAdmin(BaseModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
