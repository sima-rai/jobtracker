from django.contrib import admin
from .models import JobApplications,CustomColumn,JobCustomValue

# Register your models here.


admin.site.register([JobApplications, CustomColumn, JobCustomValue])