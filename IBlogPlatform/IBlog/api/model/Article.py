from django.db import models
from ..models import Author, Tag
from .validators import XSS_validator
from django.utils import timezone
import uuid


def get_image_upload_path(instance, filename):
    return f'images/{instance.authName} - arts/{filename}'


class Article(models.Model):
    artID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    artName = models.CharField(max_length=255, validators=[XSS_validator])
    artImg = models.ImageField(
        upload_to=get_image_upload_path, null=True, blank=True)
    artContent = models.TextField(validators=[XSS_validator])
    artCreatedAt = models.DateTimeField(auto_now_add=True)
    artUpdatedAt = models.DateTimeField(auto_now_add=True)
    artAgree = models.IntegerField(default=0)
    artDisagree = models.IntegerField(default=0)
    authID = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='articles')
    artTags = models.ManyToManyField(
        Tag, related_name='articletag', blank=True)

    def __str__(self):
        return self.artName
