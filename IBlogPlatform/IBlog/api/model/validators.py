
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Validator for authName
noSpaces_noSpecial_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message=_(
        "Name must contain only letters and numbers, no spaces or special characters.")
)

# Validator for authBio (basic XSS prevention)
XSS_validator = RegexValidator(
    regex=r'^[^<>]*$',
    message=_("Bio cannot contain HTML tags.")
)
