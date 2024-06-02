import importlib
import os
import re

from django.conf import settings
from django.db import IntegrityError

from helpers.exceptions import BaseException
from permission.helpers.permission_maps import get_permission_map
from permission.models import Permission, Role

HTTP_METHODS = ["get", "post", "put", "patch", "delete"]

REST_ACTIONS = ["create", "list", "update", "destroy", "partial_update", "retrieve"]

CREATE_PERMISSION_MSG = "Please create permission for url '{}' and method '{}' \
    at permission.models.permission."


def remove_special_characters(string):
    return string.replace("\n", "").replace("\t", "").strip()


def get_detail(action):
    """
    Get __doc__ string from action.
    """

    return remove_special_characters(action.__doc__ or "")


def intersects(list1, list2):
    if len(set(list1).intersection(set(list2))) > 0:
        return True
    else:
        return False


def is_django_function_view(url):
    # django function view
    # no cls
    if not getattr(url.callback, "cls", None) and not getattr(
        url.callback, "view_class", None
    ):
        return True
    else:
        return False


def is_django_class_view(url):
    # APIView
    # any of get/post/put/patch/delete/
    cls = getattr(url.callback, "cls", None) or getattr(
        url.callback, "view_class", None
    )
    if not cls or re.search("WrappedAPIView", str(url.callback)):
        return False

    if intersects(HTTP_METHODS, dir(cls)):
        return True
    else:
        return False


def is_rest_decorated_view(url):
    # @api_view
    # WrappedAPIView
    if re.search("WrappedAPIView", str(url.callback)):
        return True
    else:
        return False


def is_rest_model_viewset(url):
    # ModelViewSet
    # any of list/retrieve/destroy/update/partial_update and queryset is present
    try:
        cls = getattr(url.callback, "cls")
        if intersects(REST_ACTIONS, dir(cls)) and cls.queryset.model:
            return True
        else:
            return False
    except AttributeError:
        return False


def is_rest_non_model_viewset(url):
    # ViewSet
    # no list/retrieve/destroy/update/partial_update
    try:
        cls = getattr(url.callback, "cls")
        frags = url.name.split("-")
        frags.pop(0)
        action = "_".join(frags)
        if getattr(cls, action):
            if intersects(REST_ACTIONS, dir(cls)):
                return False
            else:
                return True
                # cls.queryset.model
    except (AttributeError, ValueError):
        return False


def get_django_function_view_action(url):
    return url.callback


def get_django_class_view_action(url, method):
    cls = getattr(url.callback, "cls", None) or getattr(url.callback, "view_class")
    try:
        return getattr(cls, method)
    except AttributeError:
        return None


def get_rest_decorated_view_action(url):
    return url.callback


def get_rest_model_viewset_action(url, action_name):
    cls = getattr(url.callback, "cls")
    try:
        return getattr(cls, action_name)
    except AttributeError:
        return None


def get_rest_non_model_viewset_action(url):
    cls = getattr(url.callback, "cls")
    frags = url.name.split("-")

    def get_action(frags):
        try:
            frags.pop(0)
            action_name = "_".join(frags)
            return getattr(cls, action_name)
        except AttributeError:
            return get_action(frags)

    return get_action(frags)


def user_has_permission(user, name, method):
    return Permission.objects.filter(
        name=name, method=method, roles__in=user.roles.all()
    ).exists()


def anon_has_permission(name, method):
    from permission.models import ANONYMOUS_USER_ROLE

    anon_role = Role.objects.get(name=ANONYMOUS_USER_ROLE)
    return Permission.objects.filter(
        name=name, method=method, roles__in=[anon_role]
    ).exists()


def has_permission(user, name, method):
    """
    Current user and name of permission which is usually name of a url.
    Except for rest url which is model_name-action-name. e.g. fee-retrieve
    """
    if user.is_authenticated:
        return user_has_permission(user, name, method)
    return anon_has_permission(name, method)


def get_django_function_view_permission(url):
    return [
        {"method": "any", "detail": get_detail(get_django_function_view_action(url))}
    ]


def get_django_class_view_permission(url):
    # http_methods = ["get", "post", "put", "patch", "delete", "options"]
    http_methods = ["get", "post", "put", "patch", "delete"]
    permissions = []
    for method in http_methods:
        action = get_django_class_view_action(url, method)
        if action:
            permissions.append({"method": method, "detail": get_detail(action)})
    return permissions


def get_rest_decorated_view_permission(url):
    permissions = []
    for method in url.callback.cls.http_method_names:
        if method == "options":
            continue
        permissions.append(
            {
                "method": method,
                "detail": get_detail(get_rest_decorated_view_action(url)),
            }
        )
    return permissions


def get_rest_model_viewset_permission(url):
    detail_action_map = {
        "retrieve": "get",
        "destroy": "delete",
        "update": "put",
        "partial_update": "patch",
    }
    #   "options": "options"}
    list_action_map = {"list": "get", "create": "post"}
    #   "options": "options"}
    permissions = []
    if re.match(r".*?-detail", url.name):
        for action_name in detail_action_map.keys():
            action = get_rest_model_viewset_action(url, action_name)
            if action:
                permissions.append(
                    {
                        "method": detail_action_map[action_name],
                        "detail": get_detail(action),
                    }
                )
    elif re.match(r".*?-list", url.name):
        for action_name in list_action_map.keys():
            action = get_rest_model_viewset_action(url, action_name)
            if action:
                permissions.append(
                    {
                        "method": list_action_map[action_name],
                        "detail": get_detail(action),
                    }
                )
    else:
        return get_rest_non_model_viewset_permission(url)

    return permissions


def get_rest_non_model_viewset_permission(url):
    action = get_rest_non_model_viewset_action(url)
    permissions = []
    for method in list(action.mapping.keys()):
        permissions.append(
            {
                "method": method,
                "detail": remove_special_characters(action.__doc__ or ""),
            }
        )
    return permissions


def get_permission(url):
    """
    returns map of permission name and http method.
    """
    if is_django_function_view(url):
        return get_django_function_view_permission(url)
    if is_rest_decorated_view(url):
        return get_rest_decorated_view_permission(url)
    if is_rest_model_viewset(url):
        return get_rest_model_viewset_permission(url)
    if is_rest_non_model_viewset(url):
        return get_rest_non_model_viewset_permission(url)
    if is_django_class_view(url):
        return get_django_class_view_permission(url)


def regex2keyword(m):
    if m:
        return ":{}".format(m.groups()[0])
    return None


def normalize_url(url):
    t = url.replace("^", "").replace("$", "")

    if t == "":
        return url

    if not t[0] == "/":
        t = "/{}".format(t)

    if not t[-1] == "/":
        t = "{}/".format(t)

    t = re.sub(r"\(\?P<(.*?)>.*?\)", regex2keyword, t)

    return t


def get_url_meta(url):
    """
    returns url_name, url, permission_name and detail
    """

    return {
        "name": url.name,
        "url": normalize_url(url.pattern.regex.pattern),
        "permissions": get_permission(url),
    }


def get_urls_for(app_name):
    try:
        urlpatterns = importlib.import_module("{}.urls".format(app_name)).urlpatterns
    except ImportError:
        return []

    urls = []
    for url in urlpatterns:
        url_meta = get_url_meta(url)
        if url_meta:
            urls.append(url_meta)
    return urls


def get_apps():
    dirs = next(os.walk(os.getcwd()))[1]
    return set(dirs).intersection(set(settings.INSTALLED_APPS))


def get_urls(exclude=[], filtero=""):
    apps = get_apps()
    urls = []
    for app in apps.difference(set(exclude)):
        urls.append(get_urls_for(app))

    return list(filter(lambda aurl: re.search(filtero, aurl["url"]), flatten(urls)))


def create_permissions():
    """
    Creates permissions.
    """
    Permission.objects.all().delete()
    permissions = []
    existing_actions = set()
    urls = get_urls()
    for url in urls:
        for permission in url["permissions"]:
            pair = (url["name"], permission["method"])
            if pair in existing_actions:
                continue
            else:
                existing_actions.add(pair)

            permissions.append(
                Permission(
                    name=url["name"],
                    url=url["url"],
                    method=permission["method"],
                    description=permission["detail"],
                )
            )

    try:
        Permission.objects.bulk_create(permissions)
    except IntegrityError as e:
        raise e


def get_url_for_client(user):
    url_maps = get_urls(exclude=[])

    new_map = {}
    for url_map in url_maps:
        url_name = url_map["name"]

        if not url_name:
            raise BaseException("Please name url: {}".format(url_map["url"]))

        new_map[url_name] = {"url": url_map["url"]}
        new_map[url_name]["permissions"] = {}
        for permission in url_map["permissions"]:
            method = permission["method"]
            new_map[url_name]["permissions"][method] = has_permission(
                user, url_map["name"], method
            )

    return new_map


def attach_permissions(role_name, permissions):
    """
    Attaches permissions to given role.
    """

    try:
        role = Role.objects.get(name=role_name)
    except Role.DoesNotExist:
        raise BaseException(f"Role with '{role_name}' could not be found.")

    permission_objs = []

    for permission in permissions:
        try:
            permission_objs.append(
                Permission.objects.get(name=permission[0], method=permission[1])
            )
        except Exception as e:
            raise BaseException("{}".format(permission), e)

    role.permissions.add(*permission_objs)
    role.save()


def flatten(nested_permissions):
    return [
        permission
        for permission_list in nested_permissions
        for permission in permission_list
    ]


def assign_permissions():
    """
    Assigns permissions to corresponding roles.
    """
    PERMISSION_MAP = get_permission_map()

    for role, permissions in PERMISSION_MAP.items():
        attach_permissions(role, flatten(permissions))


def update_permissions():
    """
    Creates permissions and assign them to respective roles.
    """

    create_permissions()
    assign_permissions()
    return Permission.objects.all().count()
