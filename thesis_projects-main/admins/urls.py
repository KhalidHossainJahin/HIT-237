from django.urls import include, path
from . import views

urlpatterns = [
  path('applications/', views.view_applications, name='applications'),
  path('approve_project/<int:pk>/', views.project_approve, name='project_approve'),
  path('application_details/<int:pk>/', views.application_details, name='application_details')
]