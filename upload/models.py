from django.db import models
import os

class CSVFile(models.Model):
    file_name = models.CharField(max_length=255, verbose_name='Uploaded By')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.filename()

    def filename(self):
        return os.path.basename(self.file.name)

    def get_author(self):
        return self.file_name