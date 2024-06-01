from permission.models import UserRole

from .admin_permissions import get_admin_permission_map


def get_permission_map():
    return {
        UserRole.ADMIN.value: get_admin_permission_map(),
    }
