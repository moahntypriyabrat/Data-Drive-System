from django.db import models

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=255, default="untitled Folder")
    file = models.FileField(upload_to='uploads/', default=False)

    def __str__(self):
        return self.name
