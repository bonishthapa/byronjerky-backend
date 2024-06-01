from rest_framework.versioning import BaseVersioning


class GBaseVersioning(BaseVersioning):
    default_version = "v1"

    def determine_version(self, request, *args, **kwargs):
        version = kwargs.get(self.version_param)
        return version or self.default_version
