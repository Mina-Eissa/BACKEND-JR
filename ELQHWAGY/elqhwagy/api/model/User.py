import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, verbose_name='User ID')	
    phone_numbers = models.JSONField(default=list, verbose_name='User Phone Numbers')
    profile_img = models.ImageField(upload_to='profile_imgs/', null=True, blank=True, verbose_name='User Profile Image')