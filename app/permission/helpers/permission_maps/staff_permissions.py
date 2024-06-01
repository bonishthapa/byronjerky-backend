from permission.helpers.app_permission.stock_permissions import PRODUCT_READ, ORDER_READ

GENERIC_STAFF_API = [
    PRODUCT_READ,
    ORDER_READ,
]


def get_staff_permission_map():
    return GENERIC_STAFF_API
