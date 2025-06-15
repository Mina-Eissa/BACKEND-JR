import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Validator for authName
noSpaces_noSpecial_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message=_(
        "Name must contain only letters and numbers, no spaces or special characters.")
)

class Tag(models.Model):
    id = models.UUIDField(verbose_name='Tag ID',primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(verbose_name='Tag Name',max_length=100,validators=[noSpaces_noSpecial_validator],unique=True)

    def __str__(self):
        return self.name