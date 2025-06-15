from django.db import models
from .validators import noSpaces_noSpecial_validator


class Tag(models.Model):
    tagName = models.CharField(max_length=50, unique=True, validators=[
                               noSpaces_noSpecial_validator])

    def __str__(self):
        return self.tagName
