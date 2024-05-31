from django.contrib import admin
from customUser.models import CustomUser
from projects.models import ProjectItem, ThesisSubmit


# Register your models here.

admin.site.register(ProjectItem)
# admin.site.register(CustomUser)
admin.site.register(ThesisSubmit)