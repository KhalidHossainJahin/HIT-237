from django.urls import include, path
from . import views


urlpatterns = [
  path('create/', views.studentGroup_create, name='studentGroup_create'),
  path('<int:group_id>/view', views.studentGroup_list, name='studentGroup_list'),
  path('<int:group_id>/edit', views.studentGroup_edit, name='studentGroup_edit'),
  path('<int:group_id>/delete', views.studentGroup_delete, name='studentGroup_delete'),
  path('<int:group_id>/remove_member/<int:user_id>', views.studentGroup_remove_member, name='studentGroup_remove_member'),
  path('join_group', views.join_group, name='join_group'),
  path('submit_application', views.submit_application, name='submit_application'),
  path('view_project/<int:pk>', views.view_project, name='view_project'),
]