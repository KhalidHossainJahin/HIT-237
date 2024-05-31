from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    link = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)