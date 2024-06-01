# from drf_yasg2.utils import swagger_auto_schema
# from django.utils.decorators import method_decorator


def api_document(names, tags):
    if "*" in names:
        names.remove("*")
        names.extend(
            ["list", "retrieve", "create", "update", "partial_update", "destroy"]
        )

    def deco(f):
        # for name in reversed(names):
        #     f = method_decorator(name=name, decorator=swagger_auto_schema(tags=tags))(f)
        return f

    return deco
