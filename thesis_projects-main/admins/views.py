from django.shortcuts import render, redirect
from studentGroup.models import applyProject
from projects.models import ProjectItem
from siteManagement.models import Notification

# Create your views here.

def view_applications(request):
    """Render a list of all pending project applications."""
    applications = applyProject.objects.all().order_by('is_approved')
    return render(request, 'applications.html', {'applications': applications})

def project_approve(request, pk):
    """Approve a project."""
    project = ProjectItem.objects.get(pk=pk)
    project.is_approved = True
    project.save()
    # send supervisor a notification
    Notification.objects.create(
        user=project.supervisor.user,
        message=f"Your project \"{project.title}\" has been approved.",
        link=f"/projects"
    )
    return redirect('project_list')

def application_details(request, pk):
  if request.method == 'POST':
    application = applyProject.objects.get(pk=pk)
    group = application.group
    if 'approve' in request.POST:
      application.is_approved = True
      application.is_rejected = False
      # notification
      for member in group.members.all():
        Notification.objects.create(
          user=member,
          message=f"Your application for project \"{application.project.title}\" has been approved. Now you can submit your thesis.",
          link="/submit"
        )
      Notification.objects.create(
        user=group.creator,
        message=f"Your application for project \"{application.project.title}\" has been approved. Now you can submit your thesis.",
        link="/submit"
      )
    elif 'reject' in request.POST:
      application.is_approved = False
      application.is_rejected = True
      for member in group.members.all():
        Notification.objects.create(
          user=member,
          message=f"Your application for project \"{application.project.title}\" has been rejected. Try applying for another project.",
          link="/projects"
        )
      Notification.objects.create(
        user=group.creator,
        message=f"Your application for project \"{application.project.title}\" has been rejected. Try applying for another project.",
        link="/projects"
      )
    application.save()
    # send all student group members and the creator a notification
    return redirect('applications')

  else:
    application = applyProject.objects.get(pk=pk)
    return render(request, 'application_details.html', {'application': application})