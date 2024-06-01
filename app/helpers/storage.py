from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class BaseMediaStorage(S3Boto3Storage):
    location = "media"

    BUCKET_PRIVATE = {
        "access_key": settings.PRIVATE_AWS_ACCESS_KEY_ID,
        "secret_key": settings.PRIVATE_AWS_SECRET_ACCESS_KEY,
        "bucket_name": settings.PRIVATE_AWS_STORAGE_BUCKET_NAME,
        "custom_domain": f"{settings.PRIVATE_AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com",
        "region_name": settings.PRIVATE_AWS_REGION,
    }
    BUCKET_PUBLIC = {
        "access_key": settings.AWS_ACCESS_KEY_ID,
        "secret_key": settings.AWS_SECRET_ACCESS_KEY,
        "bucket_name": settings.AWS_STORAGE_BUCKET_NAME,
        "custom_domain": f"{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com",
        "region_name": settings.AWS_REGION,
        "default_acl": "public-read",
    }

    def __init__(self, *args, **kwargs):
        scope_dict_map = {
            "private_file": self.BUCKET_PRIVATE,
            "public_file": self.BUCKET_PUBLIC,
        }

        scope = kwargs.pop("scope", "")
        if scope_dict_map.get(scope):
            kwargs.update(scope_dict_map[scope])
        super().__init__(*args, **kwargs)
