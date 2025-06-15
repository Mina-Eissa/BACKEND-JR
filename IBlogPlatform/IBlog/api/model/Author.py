from django.db import models
from django.utils import timezone
from pathlib import Path
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
# Import your validators
from .validators import noSpaces_noSpecial_validator, XSS_validator


# Assuming you have a default image in your media folder
DEFAULT_PERSONAL_IMAGE = 'images/default_personal.png'
DEFAULT_WALLPAPER_IMAGE = 'images/default_wallpaper.png'


class AuthorManager(BaseUserManager):
    def create_user(self, authEmail, authName, password=None, **extra_fields):
        if not authEmail:
            raise ValueError('Email is required')
        email = self.normalize_email(authEmail)
        user = self.model(authEmail=email, authName=authName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, authEmail, authName, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(authEmail, authName, password, **extra_fields)


class Author(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    authName = models.CharField(max_length=100, unique=True, validators=[
                                noSpaces_noSpecial_validator])
    authEmail = models.EmailField(unique=True)
    authImg = models.ImageField(upload_to='images/%Y/%m/%d/personal/',
                                default=DEFAULT_PERSONAL_IMAGE, null=True, blank=True)
    authWallpaper = models.ImageField(
        upload_to='images/%Y/%m/%d/wallpaper/', default=DEFAULT_WALLPAPER_IMAGE, null=True, blank=True)
    authBirthDate = models.DateField()
    authBio = models.TextField(validators=[XSS_validator])
    authCreatedAt = models.DateTimeField(auto_now_add=True)
    authUpdatedAt = models.DateTimeField(auto_now_add=True)
    authPassword = models.CharField(max_length=128, default="temp-password")

    # Required fields for Django auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'authEmail'  # used for login
    REQUIRED_FIELDS = ['authName']

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    @property
    def age(self):
        now = timezone.now()
        return now.year - self.authBirthDate.year - ((now.month, now.day) < (self.authBirthDate.month, self.authBirthDate.day))

    def __str__(self):
        return self.authName
