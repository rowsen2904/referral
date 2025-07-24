import random
import re
import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def generate_invite_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def validate_russian_phone(value):
    if not re.fullmatch(r'^\+7\d{10}$', value):
        raise ValidationError(
            _("The number must be in the format: +7XXXXXXXXXX"))


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Phone number is required'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_unusable_password()  # пароль не нужен
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_russian_phone]
    )
    invite_code = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
    )
    activated_invite_code = models.CharField(max_length=6, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_unique_invite_code()
        super().save(*args, **kwargs)

    def generate_unique_invite_code(self):
        while True:
            code = generate_invite_code()
            if not User.objects.filter(invite_code=code).exists():
                return code

    def get_referred_users(self):
        return User.objects.filter(activated_invite_code=self.invite_code)

    def __str__(self):
        return self.phone_number
