import os
import time

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from config.constants import UPLOAD_FILE_TYPE_IMAGE, UPLOAD_FILE_TYPE_OTHERS
from helpers.models import BaseFileUpload, BaseModel
from permission.models import UserRole


def file_upload_path(instance, filename):
    random_prefix = f"{int(time.time())}_"
    year, month, day = timezone.now().strftime("%Y,%m,%d").split(",")
    fileparts = os.path.splitext(filename)
    new_filename = slugify(f"{random_prefix}{fileparts[0]}")
    if instance.user:
        return f"{year}/u_{instance.user.id}/{month}/{day}/{new_filename}{fileparts[1]}"
    return f"{year}/common/{month}/{day}/{new_filename}{fileparts[1]}"


class Config(BaseModel):
    app = models.CharField(max_length=20, blank=False, null=False)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    feature_flag = models.BooleanField(default=True)

    class Meta:
        unique_together = ("app", "key")

    def __str__(self):
        return f"{self.app} - {self.key}"

    @classmethod
    def get_config_or_default(cls, key, app="", default=""):
        try:
            return cls.objects.get(key=key, app=app)
        except Config.DoesNotExist:
            pass
        if isinstance(default, str):
            return Config(value=default)
        return Config(meta=default)

    @classmethod
    def get_config(cls, key, app=None):
        filters = {"key": key, "is_obsolete": False}
        if app:
            filters["app"] = app
        try:
            return cls.objects.get(**filters)
        except (cls.ObjectDoesNotExist, cls.MultipleObjectsReturned):
            return None

    @classmethod
    def get_config_dict(cls, key, app=None):
        _config = cls.get_config(key, app)
        if _config:
            return _config.meta
        return {}


class FileUpload(BaseFileUpload):
    class FileType(models.TextChoices):
        OTHERS = UPLOAD_FILE_TYPE_OTHERS
        IMAGE = UPLOAD_FILE_TYPE_IMAGE

    user = models.ForeignKey(
        "autho.User",
        on_delete=models.CASCADE,
        related_name="file_uploads",
        default=None,
        null=True,
        blank=True,
    )
    file = models.FileField(upload_to=file_upload_path)
    file_type = models.CharField(
        max_length=10, choices=FileType.choices, default=FileType.OTHERS.value
    )
    is_private_to_user = models.BooleanField(default=False)

    def can_retrieve(self, user):
        if self.is_private_to_user:
            return user.id == self.user.id
        return user.iss([UserRole.ADMIN])

    def can_update(self, user):
        return user == self.user or user.iss(
            [
                UserRole.ADMIN,
            ]
        )

    def can_destroy(self, user):
        self.can_update(user)

    def can_partial_update(self, user):
        return self.can_update(user)


class ActionLog(BaseModel):
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        "autho.User",
        related_name="actionlogs",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    action = models.CharField(max_length=200, db_index=True)
    action_obj_type = models.CharField(max_length=100, blank=False, db_index=True)
    action_obj_id = models.BigIntegerField(db_index=True)

    remarks = models.TextField(null=True)
    previous_state = models.JSONField(default=dict, blank=True)
    next_state = models.JSONField(default=dict, blank=True)

    request_path = models.CharField(max_length=300, db_index=True, null=True)
    query_string = models.TextField(null=True)
    request_method = models.CharField(max_length=10, db_index=True, null=True)
    request_body = models.TextField(null=True)
    request_meta = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"User ({self.user})"

    def get_basic_info(self):
        user = self.user

        return {
            "created_on": self.created_on.strftime("%b %-d, %Y %H:%M:%S"),
            "user": f"{user.name} ({user.mobile} - {user.email})" if user else "",
            "action": self.action,
            "previous_state": self.previous_state,
            "next_state": self.next_state,
            "remarks": self.remarks,
        }

    @classmethod
    def new(
        cls,
        user,
        action,
        remarks,
        prev_state,
        next_state,
        request_meta={},
        request_body="",
        data={},
    ):
        data.update(
            {
                "user": user,
                "action": action,
                "remarks": remarks,
                "previous_state": prev_state,
                "next_state": next_state,
                "request_path": request_meta.get("PATH_INFO"),
                "query_string": request_meta.get("QUERY_STRING"),
                "remote_addr": request_meta.get("REMOTE_ADDR"),
                "request_method": request_meta.get("REQUEST_METHOD"),
                "request_body": request_body,
            }
        )
        req_meta = {k: v for k, v in request_meta.items() if k.startswith("HTTP_")}
        req_meta.update(
            {
                "DESKTOP_SESSION": request_meta.get("DESKTOP_SESSION", ""),
                "VERSION": request_meta.get("VERSION", ""),
                "SERVER_PORT": request_meta.get("SERVER_PORT", ""),
                "REMOTE_HOST": request_meta.get("REMOTE_HOST", ""),
                "CONTENT_TYPE": request_meta.get("CONTENT_TYPE", ""),
            }
        )
        data.update({"request_meta": req_meta})
        return cls.objects.create(**data)

    @classmethod
    def get_obj_action_logs(cls, action_obj):
        return cls.objects.filter(
            action_obj_type=action_obj._meta.db_table, action_obj_id=action_obj.id
        )
