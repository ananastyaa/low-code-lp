from django.db import models

# Create your models here.

class File(models.Model):
    
    path = models.FileField(upload_to= 'files/',blank=True, null=True)
    name = models.TextField()
    extension = models.CharField(max_length=255)


class Parameter(models.Model):
    file_id = models.ForeignKey('File', on_delete=models.CASCADE)
    idx = models.TextField()
    param = models.TextField()
    limit = models.TextField()
    func = models.TextField()
    criteria = models.BooleanField()