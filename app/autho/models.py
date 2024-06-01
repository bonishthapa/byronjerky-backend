from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from core.models import Config
from helpers.models import BaseModel
from helpers.tasks import send_email


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given  email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    roles = models.ManyToManyField("permission.Role", related_name="users", blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    objects = UserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_basic_info(self):
        return {"uuid": str(self.uuid), "name": self.name, "email": self.email}

    def get_roles(self):
        return list(self.roles.values_list("name", flat=True))

    def get_ui_permissions(self):
        roles = self.get_roles()
        permisssions = []
        role_permission_map = Config.get_config_or_default(
            "role_permission_map", app="autho", default={}
        ).meta
        for role in roles:
            permisssions.extend(role_permission_map.get(role, []))
        return permisssions

    def iss(self, role):
        if role is str:
            role = [role]
        role = set(role)
        roles = list(self.roles.values_list("name", flat=True))
        return len(set(roles).intersection(role)) > 0

    def send_email(self, subject, message, **kwargs):
        send_email.delay(subject, message, self.email, **kwargs)


class Customer(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    lead_time = models.IntegerField(help_text='lead time in days')
    mobile = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    @classmethod
    def new(cls, **kwargs):
        user = kwargs.pop('user', None)
        return cls.objects.create(user=user, **kwargs)

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
