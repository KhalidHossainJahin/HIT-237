from django.db import models
from customUser.models import CustomUser

# Create your models here.

class studentGroup(models.Model):
  id = models.AutoField(primary_key=True)
  groupName = models.CharField(max_length=100)
  creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  members = models.ManyToManyField(CustomUser, related_name='members', blank=True)
  join_code = models.CharField(max_length=100)
  # requested_members = models.ManyToManyField(CustomUser, related_name='requested_members', blank=True)
  def __str__(self):
    return self.groupName

class applyProject(models.Model):
  id = models.AutoField(primary_key=True)
  project = models.ForeignKey('projects.ProjectItem', on_delete=models.CASCADE)
  group = models.ForeignKey(studentGroup, on_delete=models.CASCADE)
  cv_zip_link = models.CharField(max_length=100)
  is_approved = models.BooleanField(default=False)
  is_rejected = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.group} applied for {self.project}"

