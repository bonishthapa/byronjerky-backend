from permission.helpers.app_permission.autho_permissions import PROFILE, USER_READ
from permission.helpers.app_permission.core_permissions import PRIVATE_FILE, PUBLIC_FILE

GENERIC_ADMIN_API = [
    PROFILE,
    USER_READ,
    PUBLIC_FILE,
    PRIVATE_FILE,
]


def get_admin_permission_map():
    return GENERIC_ADMIN_API
