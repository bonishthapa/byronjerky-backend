from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils import timezone

import boto3

from .managers import DefaultManager
from .model_fields import CreatedDateField, IDXField

tz = timezone.get_current_timezone()


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    idx = IDXField()
    created_date = CreatedDateField()

    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs):
        return cls.objects.create(**kwargs)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete(self, force_delete=True, **kwargs):
        if force_delete:
            super().delete(**kwargs)
        else:
            self.update(is_deleted=True)
            return self


class BaseModel(TimeStampedModel):
    """
    Soft delete model
    """

    deleted_on = models.DateTimeField(null=True, default=None, blank=True)
    is_deleted = models.BooleanField(default=False)
    meta = models.JSONField(default=dict, blank=True)
    objects = DefaultManager()

    class Meta:
        abstract = True

    def delete(self, force_delete=True, **kwargs):
        if force_delete:
            super().delete(**kwargs)
        else:
            self.update(is_deleted=True, deleted_on=timezone.now())
            return self


class SingletonModel(BaseModel):
    """
    Singleton Model
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class BaseFileUpload(BaseModel):
    @property
    def accessible_file_path(self):
        if not self.is_private_to_user:
            return self.file.url

        name = f"media/{self.file.name}"
        s3client = boto3.client(
            "s3",
            aws_access_key_id=settings.PRIVATE_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.PRIVATE_AWS_SECRET_ACCESS_KEY,
            region_name=settings.PRIVATE_AWS_REGION,
        )

        signed_url = s3client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.PRIVATE_AWS_STORAGE_BUCKET_NAME, "Key": name},
            ExpiresIn=settings.AWS_EXPIRESIN,
            HttpMethod="GET",
        )
        return signed_url

    class Meta:
        abstract = True
