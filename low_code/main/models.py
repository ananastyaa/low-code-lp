from django.db import models

# Create your models here.

class Data(models.Model):
    name_param = models.CharField(max_length=255)
    name_idx = models.CharField(max_length=255, blank=False, null=False)
    file = models.FileField(upload_to= 'files/',null=True)

    def __repr__(self):
        return 'Resume(%s, %s)' % (self.name_idx, self.file)

    def __str__ (self):
        return self.name_idx