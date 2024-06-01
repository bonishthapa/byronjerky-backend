from django.urls import resolve

from rest_framework.permissions import BasePermission

from helpers.exceptions import BaseException

from .permissions import has_permission


class GBasePermission(BasePermission):
    def has_permission(self, request, view):
        url_name = resolve(request.path_info).url_name
        method = request.method.lower()
        return has_permission(request.user, url_name, method)

    def has_object_permission(self, request, view, obj):
        try:
            model = view.queryset.model or view.model
        except AttributeError:
            raise BaseException(
                "It seems the view is not associated with any model.\
Please overwrite this method as per need."
            )

        try:
            method_name = "can_{}".format(view.action or request.method.lower())
            return not not getattr(obj, method_name)(view.request.user)
        except AttributeError as e:
            print(e)
            raise BaseException("Please implement {}.{}.".format(model, method_name))
