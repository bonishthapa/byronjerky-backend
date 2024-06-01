from enum import Enum, unique

from django.db import models

from helpers.models import BaseModel


@unique
class UserRole(Enum):
    ADMIN = "Admin"
    ANONYMOUS = "Anonymous"
    STAFF = "Staff"

    @classmethod
    def get(cls, key):
        enum_obj = getattr(cls, key, None)
        return enum_obj.value


class Permission(BaseModel):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    method = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = (("name", "method"),)

    def __str__(self):
        return "{} ; {} ; {}".format(self.name, self.url, self.method)


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)
    precedence = models.IntegerField(default=0)
    badge_url = models.URLField(null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    def get_basic_info(self):
        return {"idx": self.idx, "name": self.name, "badge_url": self.badge_url}

    def __str__(self):
        return self.name
