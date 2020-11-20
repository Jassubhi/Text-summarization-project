from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import media, request
from django.conf import settings
import datetime


class Document(models.Model):
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, default='Document_name')
    date = models.DateField("Date", default=datetime.date.today)
    file = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc'])
    ])

    objects = models.Manager()

    def __str__(self):
        return self.name

