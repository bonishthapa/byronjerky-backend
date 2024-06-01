from permission.models import UserRole

from .admin_permissions import get_admin_permission_map
from .staff_permissions import get_staff_permission_map


def get_permission_map():
    return {
        UserRole.ADMIN.value: get_admin_permission_map(),
        UserRole.STAFF.value: get_staff_permission_map(),
    }
