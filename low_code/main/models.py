from django.forms import ValidationError
import magic

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

# Create your models here.

class Project(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    name = models.TextField()
    desc = models.TextField()

class File(models.Model):
    project_id = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)
    path = models.FileField(upload_to='files/', blank=True, null=True)
    name = models.TextField()
    extension = models.CharField(max_length=255)

class Parameter(models.Model):
    file_id = models.ForeignKey('File', on_delete=models.CASCADE)
    idx = models.TextField()
    param = models.TextField()
    limit = models.TextField()
    func = models.TextField()

    CRITERIA_CHOICES = [(False, 'Минимизация'), (True, 'Максимизация')]
    criteria = models.BooleanField(choices=CRITERIA_CHOICES)