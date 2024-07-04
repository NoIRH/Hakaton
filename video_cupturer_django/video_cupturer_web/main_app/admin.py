from django.contrib import admin

from .models import UserFileUpload
from.models import UserFileDetected

admin.site.register(UserFileUpload)
admin.site.register(UserFileDetected)