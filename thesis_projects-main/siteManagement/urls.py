from django.urls import path, include
from . import views

urlpatterns = [
  path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read')
]