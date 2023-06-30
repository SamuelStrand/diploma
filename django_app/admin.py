from django.contrib import admin

from django_app import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Profile)
admin.site.register(models.PostComment)
admin.site.register(models.ProfileComment)
admin.site.register(models.Complaint)
