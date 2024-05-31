# thesis_projects/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('new/', views.project_create, name='project_create'),
    path('<int:pk>/edit/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('about/', views.about, name='about'),
    path('accounts/', include('allauth.urls')),
    path('register/', views.register, name='register'),
    path('submit/', views.thesis_submit, name='thesis_submit'),
    path('submissions/', views.submissions, name='submissions'),
    path('setUserType/', views.setUserType, name='setUserType'),
    path('pending_projects', views.pending_projects, name='pending_projects'),
]
