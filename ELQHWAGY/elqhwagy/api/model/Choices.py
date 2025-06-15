from django.db import models

class Roles(models.TextChoices):
    ADMIN = 'ADMIN', 'ADMIN'
    USER = 'USER', 'USER'
    STAFF = 'STAFF', 'STAFF'

class StaffRoles(models.TextChoices):
    CASHIER = 'CASHIER', 'CASHIER'
    BARISTA = 'BARISTA', 'BARISTA'
    WAITER = 'WAITER', 'WAITER'

class Categories(models.TextChoices):
    DRINK = 'DRINK', 'DRINK'
    SMOKE = 'SMOKE','SMOKE'

