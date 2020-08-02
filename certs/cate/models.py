from django.db import models
from django.contrib.auth.models import User
import csv


# Create your models here.
class Trainee(models.Model):
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class File(models.Model):
    file_n = models.FileField(upload_to='files')
    uploaded = models.BooleanField(default=False)

    @property
    def filename(self):
        return self.audio_file.path

    def __str__(self):
        return '{}'.format(self.file_n)
