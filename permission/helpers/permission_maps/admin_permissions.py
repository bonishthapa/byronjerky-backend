from permission.helpers.app_permission.autho_permissions import PROFILE, USER_READ, CUSTOMER, SEARCH_CUSTOMER, USER
from permission.helpers.app_permission.core_permissions import PRIVATE_FILE, PUBLIC_FILE
from permission.helpers.app_permission.stock_permissions import PRODUCT, ORDER, SEARCH_PRODUCT

GENERIC_ADMIN_API = [
    PROFILE,
    USER_READ,
    PUBLIC_FILE,
    PRIVATE_FILE,
    PRODUCT,
    ORDER,
    CUSTOMER,
    SEARCH_CUSTOMER,
    SEARCH_PRODUCT,
    USER,
]


def get_admin_permission_map():
    return GENERIC_ADMIN_API
