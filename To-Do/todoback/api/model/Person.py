import uuid
import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

# Assuming you have a default image in your media folder
DEFAULT_PERSONAL_IMAGE = 'images/default_personal.png'
DEFAULT_WALLPAPER_IMAGE = 'images/default_wallpaper.png'


def validate_safe_name(value):
    if not re.match(r'^[a-zA-Z0-9\-]+$', value):
        raise ValidationError(
            "Name must only contain letters, numbers, or hyphens.")


class Person(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_safe_name],
        verbose_name="username"
    )
    email = models.EmailField(unique=True)
    personnal_img = models.ImageField(
        upload_to='profiles/', default=DEFAULT_PERSONAL_IMAGE, blank=True)
    wallpaper_img = models.ImageField(
        upload_to='wallpapers/', default=DEFAULT_WALLPAPER_IMAGE, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Ensure email is always lowercase for uniqueness
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (
                    self.birth_date.month, self.birth_date.day)
            )
        return 0
