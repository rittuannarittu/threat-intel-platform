from django.contrib import admin
from .models import IOC, Source, Correlation
admin.site.register([IOC, Source, Correlation])
