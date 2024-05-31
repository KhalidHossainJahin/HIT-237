from .models import Notification
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def notifications(request):
  if request.user.is_authenticated:
    """Render a list of all notifications for the user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    no_of_unseen = Notification.objects.filter(user=request.user, seen=False).count()
    return {'notifications': notifications, 'no_of_unseen': no_of_unseen}
  else:
    return {'notifications': []}