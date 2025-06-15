from django.db import models

class Client(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, verbose_name='Client Name')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Client Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Client Phone')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.name