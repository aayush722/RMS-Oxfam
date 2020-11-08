from django.contrib import admin
# <<<<<<< HEAD
# from jobsapp.models import Job
# # Register your models here.
# admin.site.register(Job)

from jobsapp.models import UserDetials, Applicant, Job
# Register your models here.

admin.site.register(UserDetials)
admin.site.register(Applicant)
admin.site.register(Job)

