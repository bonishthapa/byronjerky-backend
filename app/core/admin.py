from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from helpers.admin import BaseModelAdmin

from .models import Config, FileUpload


@admin.register(Config)
class ConfigAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "key",
        "value",
        "meta",
        "is_deleted",
    )
    list_filter = (
        "is_deleted",
        "deleted_on",
    )

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(FileUpload)
class FileUploadAdmin(BaseModelAdmin):
    list_display = ("id", "user", "file")
    list_filter = ("user",)
