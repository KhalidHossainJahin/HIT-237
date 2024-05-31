from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Notification

# Create your views here.

def mark_as_read(request, notification_id):
  """Mark a notification as read."""
  notification = Notification.objects.get(id=notification_id)
  notification.seen = True
  notification.save()
  return redirect(notification.link)