import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.template.context_processors import media, request


class Document(models.Model):
    name = models.CharField(max_length=255, default='Document_name')
    date = models.DateField()
    file = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc'])
    ])

    def __str__(self):
        return self.name
