USER_READ = [
    ("users-list", "get"),
    ("users-detail", "get"),
]

PROFILE = [
    ("user-profile", "get"),
]

CUSTOMER_READ = [
    ("customer-list", "get"),
    ("customer-detail", "get"),
]

CUSTOMER = CUSTOMER_READ + [
    ("customer-list", "post"),
    ("customer-detail", "put"),
    ("customer-detail", "delete"),
]

SEARCH_CUSTOMER = [
    ("customer-all", "get"),
]
