from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('unit_coordinator', 'Unit Coordinator'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)