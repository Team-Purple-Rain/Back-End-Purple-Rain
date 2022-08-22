from django.contrib import admin
from .models import HikingSession, HikingCheckPoint
# Register your models here.

admin.site.register(HikingSession)
admin.site.register(HikingCheckPoint)