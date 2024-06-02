PUBLIC_FILE_READ = [
    ("public-file-upload-list", "get"),
    ("public-file-upload-detail", "get"),
]
PUBLIC_FILE = PUBLIC_FILE_READ + [
    ("public-file-upload-list", "post"),
    ("public-file-upload-detail", "delete"),
    ("public-file-upload-detail", "put"),
    ("public-file-upload-detail", "patch"),
]

PRIVATE_FILE_READ = [
    ("private-file-upload-list", "get"),
    ("private-file-upload-detail", "get"),
]
PRIVATE_FILE = PRIVATE_FILE_READ + [
    ("private-file-upload-list", "post"),
    ("private-file-upload-detail", "delete"),
    ("private-file-upload-detail", "put"),
    ("private-file-upload-detail", "patch"),
]
