USER_READ = [
    ("users-list", "get"),
    ("users-detail", "get"),
    ("users-staff-list", "get"),
]

USER = USER_READ + [
    ("users-list", "post"),
    ("users-detail", "patch"),
    ("users-detail", "delete"),
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
    ("customer-detail", "patch"),
    ("customer-detail", "delete"),
]

SEARCH_CUSTOMER = [
    ("customer-all", "get"),
]
