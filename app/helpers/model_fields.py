from datetime import date
from enum import Enum, unique

from django.db import models
from django.utils import timezone

from shortuuid import ShortUUID


@unique
class IDXPrefix(Enum):
    autho_user = "USR"

    core_config = "cfg"
    core_fileupload = "FUP"
    permission_permission = "PRM"
    permission_role = "ROL"

    @classmethod
    def get(cls, key):
        enum_obj = getattr(cls, key, None)
        return enum_obj.value


class IDXField(models.CharField):
    description = "A short UUID field."
    alphabet = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

    def __init__(self, *args, **kwargs):
        self.length = kwargs.pop("length", 8)

        if "max_length" not in kwargs:
            # If `max_length` was not specified, set it here.
            kwargs["max_length"] = 15

        kwargs.update({"unique": True, "editable": False, "blank": True})

        super().__init__(*args, **kwargs)

    def _generate_uuid(self, _prefix):
        """Generate a short random string."""
        _year = str(date.today().year)[2:]
        _uuid = ShortUUID(alphabet=self.alphabet).random(length=self.length)
        return f"{_prefix}{_year}{_uuid}".upper()

    def pre_save(self, instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """

        value = super().pre_save(instance, add)
        if not value:
            _table_name = instance._meta.db_table
            prefix = IDXPrefix.get(_table_name)
            value = self._generate_uuid(prefix)
            setattr(instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["length"] = self.length
        kwargs.pop("default", None)
        return name, path, args, kwargs


class CreatedDateField(models.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.update({"editable": False, "db_index": True})
        super().__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        value = super().pre_save(instance, add)
        if not value:
            created_on = getattr(instance, "created_on", None) or timezone.now()
            value = timezone.localdate(created_on)
        return value
