from django.shortcuts import render, redirect
from .models import studentGroup
from customUser.models import CustomUser
from django.http import HttpResponse
import random, string
from django.contrib.auth.models import User
from projects.models import ProjectItem
from .models import applyProject
from .forms import applyProjectForm
from django.db.models import Q
from siteManagement.models import Notification

# Create your views here.

def studentGroup_create(request):
  if request.method == 'POST':
    groupName = request.POST['groupName']
    try:
      creator = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
      print(f"User {request.user} does not exist")
      return HttpResponse('User does not exist')

    # make a unique join code
    join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    studentGroup.objects.create(groupName=groupName, creator=creator, join_code=join_code)
    group_id = studentGroup.objects.get(groupName=groupName, creator=creator).id
    return redirect('studentGroup_list', group_id=group_id)
  else:
    return render(request, 'studentGroup.html')

def studentGroup_list(request, group_id):
  # check if the user is a member of the group or the creator of the group
  group = studentGroup.objects.get(id=group_id)
  if request.user == group.creator or request.user in group.members.all():
    is_creator = request.user == group.creator
    return render(request, 'studentGroup_list.html', {
      'group': group,
      'is_creator': is_creator,
      'edit': False,
    })
  else:
    return HttpResponse('You are not a member of this group')

def studentGroup_edit(request, group_id):
  group = studentGroup.objects.get(id=group_id)
  if request.user == group.creator:
    if request.method == 'POST':
      groupName = request.POST['groupName']
      group.groupName = groupName
      group.save()
      for member in group.members.all():
        Notification.objects.create(user=member, message=f"Your group name has been updated to \"{group.groupName}\" by the creator.", link=f"/studentGroup/{group_id}")
      return redirect('studentGroup_list', group_id=group_id)

    return render(request, 'studentGroup_list.html', {
      'group': group,
      'edit': True,
      'is_creator': True,
    })
  else:
    return HttpResponse('You are not the creator of this group')

def studentGroup_delete(request, group_id):
  group = studentGroup.objects.get(id=group_id)
  if request.user == group.creator:
    for member in group.members.all():
      Notification.objects.create(user=member, message=f"Your group \"{group.groupName}\" has been deleted by the creator.", link="/studentGroup/create")
    group.delete()
    return redirect('studentGroup_create')
  else:
    return HttpResponse('You are not the creator of this group')

# def studentGroup_add_member(request, group_id, user_id):
#   group = studentGroup.objects.get(id=group_id)
#   if request.user == group.creator:
#     if request.method == 'POST':
#       member = User.objects.get(id=user_id)
#       if member not in group.members.all():
#         group.members.add(member)
#       else:
#         return HttpResponse('User is already a member of this group')

#     return redirect('studentGroup_list', group_id=group_id)
#   else:
#     return HttpResponse('You are not the creator of this group')

def join_group(request):
  if request.method == 'POST':
    join_code = request.POST['join_code']
    try:
      group = studentGroup.objects.get(join_code=join_code)
    except:
      return HttpResponse('Invalid join code')

    if group in studentGroup.objects.filter(members=request.user):
      return HttpResponse('You are already a member of this group')
    group.members.add(request.user)
    for member in group.members.all():
      Notification.objects.create(
        user=member,
        message=f"\"{request.user}\" have been added to the group \"{group.groupName}\".",
        link=f"/studentGroup/{group.id}/view"
      )
    Notification.objects.create(
      user=group.creator,
      message=f"\"{request.user}\" has joined the group \"{group.groupName}\".",
      link=f"/studentGroup/{group.id}"
    )
    return redirect('studentGroup_list', group_id=group.id)
  else:
    return render(request, 'join_group.html')

def studentGroup_remove_member(request, group_id, user_id):
  group = studentGroup.objects.get(id=group_id)
  if request.user == group.creator:
    member = CustomUser.objects.get(id=user_id)
    if member in group.members.all():
      group.members.remove(member)
      for rem_members in group.members.all():
        Notification.objects.create(user=rem_members, message=f"\"{member}\" has been removed from the group \"{group.groupName}\" by the creator.", link=f"/studentGroup/{group_id}")
      return redirect('studentGroup_list', group_id=group_id)
    else:
      return HttpResponse('User is not a member of this group')
  else:
    return HttpResponse('You are not the creator of this group')

def submit_application(request):
  if request.method == 'POST':
    group_id = request.POST['group_id']
    project_id = request.POST['project_id']
    group = studentGroup.objects.get(id=group_id)
    if group.members.count() < 2:
      return HttpResponse('Not enough members in the group to apply for a project. At least 2 members are required.')
    project = ProjectItem.objects.get(id=project_id)
    applyProject.objects.create(group=group, project=project)
    # send the supervisor a notification
    Notification.objects.create(user=project.supervisor.user, message=f"Group \"{group.groupName}\" has applied for your project \"{project.title}\"", link=f"/projects/{project_id}")

    return redirect('project_list')
  else:
    return HttpResponse('Invalid request')


def view_project(request, pk):
  if request.method == 'POST':
    # Get the group that the logged-in user belongs to
    group = studentGroup.objects.get(Q(members=request.user) | Q(creator=request.user))
    project = ProjectItem.objects.get(id=pk)
    cv_zip_link = request.POST['cv_zip_link']
    applied_project = applyProject.objects.create(group=group, project=project, cv_zip_link=cv_zip_link, is_approved=False)
    # send the supervisor a notification
    Notification.objects.create(
      user=project.supervisor.user,
      message=f"Group \"{group.groupName}\" has applied for your project \"{project.title}\"",
      link=f"/admins/application_details/{applied_project.id}"
    )
    return redirect('view_project', pk=pk)
  else:
    group_applied = applyProject.objects.filter(Q(group__members=request.user) | Q(group__creator=request.user))
    project = ProjectItem.objects.get(id=pk)
    form = applyProjectForm(initial={'project': project})
    if (group_applied.filter(project=pk).exists()):
      return render(request, 'view_project.html', {
        'project': project,
        'form': form,
        'is_applied': True,
      })
    else:
      return render(request, 'view_project.html', {
        'project': project,
        'form': form,
        'is_applied': False,
      })
