# projects/models.py
from django.db import models
from admins.models import supervisors, unitCoordinators
from customUser.models import CustomUser
from studentGroup.models import applyProject, studentGroup

class ProjectItem(models.Model):
    title = models.CharField(max_length=200)
    supervisor = models.ForeignKey(supervisors, on_delete=models.CASCADE)
    brief_description = models.TextField()
    full_description = models.TextField()
    topic_number = models.IntegerField(unique=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class ThesisSubmit(models.Model):
    group = models.ForeignKey(studentGroup, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectItem, on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='thesis_submissions/')
    is_approved = models.BooleanField(default=None, null=True)

    def __str__(self):
        return f'{self.group} - {self.project.title}'
