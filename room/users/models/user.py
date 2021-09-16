from typing import Optional
from django.db import models

from django.contrib.auth.models import (
    BaseUserManager as BUM,
    PermissionsMixin,
    AbstractBaseUser,
)

from common.models import BaseModel


class UserManager(BUM):
    def normalize_email(self, *, email: str) -> str:
        return super().normalize_email(email.lower())

    def _create_user(
        self,
        *,
        email: str,
        is_active: bool = True,
        is_admin: bool = True,
        is_superuser: bool = False,
        password: Optional[str] = None,
        **extra_fields,
    ) -> "User":
        # email can't be null or ""
        if not email:
            raise ValueError("Users must have an email id")

        # creating User model object using the provided data
        user: User = self.model(
            email=self.normalize_email(email=email),
            is_active=is_active,
            is_admin=is_admin,
            **extra_fields,
        )

        # if password is None then set password hash
        # as a value that will never be a valid hash
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(raw_password=password)

        # used for validation of the user Model
        # checks uniqueness, validness of values etc.
        # raise a ValidationError for any errors that occur
        user.full_clean()

        if is_superuser:
            user.is_superuser = True

        # save the user to database
        user.save(using=self._db)

        return user

    def create_user(
        self,
        email: str,
        is_active: bool = True,
        is_admin: bool = False,
        password: Optional[str] = None,
        **extra_fields,
    ) -> "User":
        return self._create_user(
            email=email,
            is_active=is_active,
            is_admin=is_admin,
            password=password,
            **extra_fields,
        )

    def create_superuser(
        self,
        email: str,
        password: Optional[str],
        **extra_fields,
    ) -> "User":
        return self._create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
            is_superuser=True,
            **extra_fields,
        )


class User(BaseModel, PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email field",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects: UserManager = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin
