from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """ Create and save new user """
    def create_user(self, email, password=None, **extra_fields):
        # 1. Create a User
        # 1.1 check if the email exist if not raise Value error
        if not email:
            raise ValueError("User must have an email address")
        # 1.2 Create user with passed parameters
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        # 1.3 set the password
        user.set_password(password)
        # 2. Save the User
        # using=self._db to make it work with different dbs
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and Save Superuser """
        # 1. create user using create_user fundtion
        user = self.create_user(
            email=email,
            password=password
        )
        # 2. set the staff and superuser permission
        user.is_staff = True
        user.is_superuser = True
        # 3. save the user
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for receipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
