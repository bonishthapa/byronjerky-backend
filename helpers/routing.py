from django.core.exceptions import ImproperlyConfigured
from django.urls import re_path

from rest_framework.routers import SimpleRouter

from helpers.versioning import GBaseVersioning


def api_url(pattern, *args, **kwargs):
    if pattern.startswith("^api/"):
        suffix = pattern[5:]
    elif "api" in pattern:
        raise ImproperlyConfigured(
            "Expected the pattern to start with '^api/'" f"got '{pattern}' instead."
        )
    else:
        suffix = pattern[1:]
    versioned_pattern = rf"^api/(?P<version>v2)/{suffix}"
    return re_path(pattern, *args, **kwargs), re_path(
        versioned_pattern, *args, **kwargs
    )


def api_urlpatterns(pairs):
    flat = []
    for u1, u2 in pairs:
        flat.append(u1)
        flat.append(u2)
    return flat


class BaseSimpleRouter(SimpleRouter):
    """
    Extend the rest framework router to allow easy
    registration of v1 and v2 urls.
    """

    def register(self, prefix, viewset, base_name=None):
        if getattr(viewset, "versioning_class", None) != GBaseVersioning:
            raise ImproperlyConfigured(
                "To use BaseSimpleRouter, you either subclass GBaseVersioning "
                "or set 'versioning_class = GBaseVersioning', please. "
                f"While registering '{viewset.__name__}'"
            )

        splitted = prefix.split("/")
        if len(splitted) == 0:
            raise ImproperlyConfigured(
                "BaseSimpleRouter prefix expected either in '<prefix1>/<prefix2>' "
                "or just <prefix> format but got "
                f"'{prefix}' instead. While registering '{viewset.__name__}'"
            )
        elif len(splitted) == 1:
            # give default prefix with viewsets without prefix
            prefix1, *prefix2 = "api", splitted[0]
        else:
            prefix1, *prefix2 = splitted

        prefix2 = "/".join(prefix2)

        versioned_prefix = rf"{prefix1}/(?P<version>v2)/{prefix2}"
        self._register(prefix, viewset, base_name=base_name)
        self._register(versioned_prefix, viewset, base_name=base_name)

    def _register(self, prefix, viewset, base_name=None):
        super().register(prefix, viewset, basename=base_name)
