import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .Person import Person
from .Tag import Tag

# Validator for text (basic XSS prevention)
XSS_validator = RegexValidator(
    regex=r'^[^<>]*$',
    message=_("Cannot contain HTML tags.")
)


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = 'PENDING', 'PENDING'
        COMPLETED = 'COMPLETED', 'COMPLETED'
        IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
        PASSED = 'PASSED', 'PASSED'

    class TaskPriority(models.TextChoices):
        LOW = 'LOW', 'LOW'
        MED = 'MED', 'MED'
        HIGH = 'HIGH', 'HIGH'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          verbose_name='Task ID', editable=False)
    name = models.CharField(max_length=100, verbose_name='Task Name', validators=[
                            XSS_validator], unique=True)
    description = models.TextField(
        verbose_name='Task Description', validators=[XSS_validator])
    status = models.CharField(verbose_name='Task Status',
                              choices=TaskStatus.choices, default=TaskStatus.PENDING, max_length=20)
    priority = models.CharField(verbose_name='Task Priority',
                                choices=TaskPriority.choices, default=TaskPriority.LOW, max_length=20)
    deadline = models.DateTimeField(verbose_name='Task Deadline')
    create = models.DateTimeField(
        verbose_name='Task Create', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Task Update', auto_now=True)
    personid = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='person_tasks')
    tags = models.ManyToManyField(Tag, related_name='task_tags',blank=True, verbose_name='Task Tags')

    def __str__(self):
        return self.name

       