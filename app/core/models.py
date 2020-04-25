from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.utils import timezone
import uuid
import os


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


class UserManager(BaseUserManager):
    def create_user(self, public_name, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        if not public_name:
            raise ValueError('Users must have a username')
        user = self.model(public_name=public_name.lower(),
                          email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user('superuser', email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def update_login(self, email=None):
        if email:
            user = self.get_by_natural_key(email)
            #user.last_login = timezone.now
            # user.save(using=self._db)
            return user
        return None


class User(AbstractBaseUser, PermissionsMixin):
    """A custom user model that supports using email instead of username"""
    public_name = models.CharField(
        max_length=30, unique=True)  # Treated as a username
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_foodtruck = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now, editable=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
