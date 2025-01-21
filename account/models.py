from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.manager import CustomUserManager
from shared.models import TimeStampedModel


class Users(AbstractUser,TimeStampedModel):
    username = None
    full_name = models.CharField(max_length=255, )
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('User', 'User'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default='User'
                            )

    phone_number = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="Phone Number",
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Avatar"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


