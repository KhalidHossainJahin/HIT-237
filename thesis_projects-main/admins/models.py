from django.db import models
# import django user
from customUser.models import CustomUser

# Create your models here.

class supervisors(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class unitCoordinators(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username