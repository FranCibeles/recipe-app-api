"""
    Database Models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """ Manager for Users """

    def create_user(self, email, password=None, **extra_field):
        """ Create, save and return a new user """

        if not email:
            raise ValueError('User must have an email address')
        # self.model is the way to access the db -> Django makes it through the ORM
        user = self.model(email=self.normalize_email(email), **extra_field)

        # Takes the password and encrypts the password with a hash
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """ Create and return a superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # To assign the User Manage
    objects = UserManager()

    # Field used for authentication
    USERNAME_FIELD = 'email'
