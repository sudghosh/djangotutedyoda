from django.db import models

# Create your models here.

class Csvs(models.Model):
    file_name = models.FileField(upload_to='csvs', max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=False)

    def __str__(self):
        return f'file-{self.id} {self.file_name}'