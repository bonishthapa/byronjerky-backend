PRODUCT_READ = [
    ("products-list", "get"),
    ("products-detail", "get"),
]

PRODUCT = PRODUCT_READ + [
    ("products-list", "post"),
    ("products-detail", "delete"),
    ("products-detail", "put"),
    ("products-detail", "patch"),
]

ORDER_READ = [
    ("orders-list", "get"),
    ("orders-detail", "get"),
]

ORDER = ORDER_READ + [
    ("orders-list", "post"),
    ("orders-detail", "delete"),
    ("orders-detail", "put"),
    ("orders-detail", "patch"),
]