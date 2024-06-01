from django.db import models


class DefaultQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class DefaultManager(models.Manager):
    def get_queryset(self):
        return DefaultQuerySet(self.model, using=self._db)  # Important!

    def active(self):
        return self.get_queryset().active()

    def deleted(self):
        return self.get_queryset().deleted()
