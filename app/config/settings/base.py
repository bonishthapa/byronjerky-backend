import os
from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-67*5x(2cz6(9w9rp$ssym6zp&r_k4uahjqejw4fmgaa#ita=6b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False)


ALLOWED_HOSTS = ["*"]


# Application definition

DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "django_rest_passwordreset",
    "corsheaders",
    "storages",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
    "django_filters",
    "drf_yasg2",
    "django_json_widget",
    "django_summernote",
]

LOCAL_APPS = [
    "core",
    "autho",
    "permission",
    "stock",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

CORS_ORIGIN_WHITELIST = (
    "http://localhost:8080",
    "http://localhost:8888",
    "http://127.0.0.1:8000",
    "http://192.168.1.94:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://localhost:3000",
)
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "content-disposition",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = config("STATIC_URL", default="/static/")
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "static_root"


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "autho.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "helpers.pagination.BasePagination",
    "DEFAULT_FILTER_BACKENDS": (
        "helpers.filter_mixins.BaseDjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "helpers.authentication.BaseTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# General Email settings
EMAIL_BACKEND = config("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", "hello@sparrowsms.com")

# Settings for SMTP Backend
EMAIL_HOST = config("EMAIL_HOST", "")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = config("EMAIL_PORT", "")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", "")

# Settings for SES Backend
AWS_SES_ACCESS_KEY_ID = config("AWS_SES_ACCESS_KEY_ID", "")
AWS_SES_SECRET_ACCESS_KEY = config("AWS_SES_SECRET_ACCESS_KEY", "")
AWS_SES_REGION_NAME = config("AWS_SES_REGION_NAME", "")
AWS_SES_REGION_ENDPOINT = config("AWS_SES_REGION_ENDPOINT", "")

# AWS Settings
AWS_REGION = config("AWS_REGION", "")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = "s3-%s.amazonaws.com/%s" % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)

PRIVATE_AWS_REGION = config("PRIVATE_AWS_REGION", "")
PRIVATE_AWS_ACCESS_KEY_ID = config("PRIVATE_AWS_ACCESS_KEY_ID", "")
PRIVATE_AWS_SECRET_ACCESS_KEY = config("PRIVATE_AWS_SECRET_ACCESS_KEY", "")
PRIVATE_AWS_STORAGE_BUCKET_NAME = config("PRIVATE_AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = "s3-%s.amazonaws.com/%s" % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
AWS_LOCATION = config("AWS_LOCATION", "kumaripati_static")
AWS_EXPIRESIN = 180

# Add This in server Settings

# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATIC_URL = f"{AWS_STORAGE_BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{AWS_LOCATION}/"
# DEFAULT_FILE_STORAGE = "config.helpers.storage.MediaStorage"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": [
            f'{config("REDIS_HOST")}:{config("REDIS_PORT")}',
        ],
    }
}

IS_STAGING_SERVER = False
