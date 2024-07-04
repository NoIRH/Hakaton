from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class UserFileUpload(models.Model):
    filename = models.FileField()
    filepath = models.FilePathField()
    fileurl = models.URLField()
    date_upload = models.DateTimeField(default=timezone.now)
    master = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename

class UserFileDetected(models.Model):
    filename = models.FileField()
    filepath = models.FilePathField()
    fileurl = models.URLField()
    fileurl_master_file = models.URLField()
    date_detected = models.DateTimeField(default=timezone.now)
    master = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename
