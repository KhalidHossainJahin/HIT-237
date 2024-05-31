# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import ProjectItem, ThesisSubmit
from customUser.forms import CustomUserCreationForm
from .forms import ProjectItemForm, ThesisSubmitForm
from django.contrib.auth import login
from django.http import HttpResponse
from admins.models import supervisors, unitCoordinators
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from siteManagement.models import Notification



def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def about(request):
    """Render the about page with team member details."""
    return render(request, 'about.html')

def project_list(request):
    """Render a list of all approved thesis projects."""
    projects = ProjectItem.objects.filter(is_approved=True)
    return render(request, 'project_list.html', {'projects': projects})

def pending_projects(request):
    """Render a list of all pending thesis projects."""
    projects = ProjectItem.objects.filter(is_approved=False)
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_create(request):
  if request.user.is_authenticated:
    """Create a new project item."""
    if request.user.user_type == 'supervisor':
      print(f"User type: {request.user.user_type}")
      if request.method == 'POST':
          form = ProjectItemForm(request.POST)
          if form.is_valid():
              form.save()
              unit_coordinator = unitCoordinators.objects.all()
              for coordinator in unit_coordinator:
                Notification.objects.create(
                  user=coordinator.user,
                  message=f"A new project has been submitted by Supervisor: \"{request.user}\". Please review the project.",
                  link = "/pending_projects"
                )
              return redirect('project_list')
      else:
          form = ProjectItemForm(initial={'supervisor': supervisors.objects.get(user=request.user)})
      return render(request, 'project_form.html', {'form': form})
    else:
      return HttpResponse(
        f"A {request.user.user_type} does not have permission to create a project.</br> \
        <h3>Back to <a href='/'>home</a> </h3>"
      )
  else:
    return redirect('login')

@login_required
def project_update(request, pk):
    """Update an existing project item."""
    project = get_object_or_404(ProjectItem, pk=pk)
    if request.method == 'POST':
        form = ProjectItemForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectItemForm(instance=project)
        project = ProjectItem.objects.get(pk=pk)
        print(f"Project approved: {project.is_approved}")
    return render(request, 'project_form.html', {
      'form': form,
      'project': project
    })

@login_required
def project_delete(request, pk):
    """Delete a project item."""
    project = get_object_or_404(ProjectItem, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})

def project_details(request, title):
    """Render the detail page for a specific project."""
    project = next((p for p in ProjectItem.objects.all() if p.title.lower() == title.lower()), None)
    if not project:
        raise Http404("Project not found")
    context = {'project': project}
    return render(request, 'project_details.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def thesis_submit(request):
    if request.method == 'POST':
        form = ThesisSubmitForm(request.POST or None, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            # send notification to the project supervisor
            project = form.cleaned_data['project']
            supervisor = project.supervisor.user
            Notification.objects.create(
              user=supervisor,
              message=f"Group \"{form.cleaned_data['group'].groupName}\" has submitted their thesis for your project \"{project.title}\"",
              link = "/submissions"
            )
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = ThesisSubmitForm(request.POST or None, user=request.user)
    return render(request, 'thesis_submit.html', {'form': form})

@login_required
def submissions(request):
  if request.method == 'POST':
    if request.user.user_type == 'supervisor':
      submission = ThesisSubmit.objects.get(pk=request.POST['submission_id'])
      if 'approve' in request.POST:
        submission.is_approved = True
        submission.save()
        # send notification to all group members and creator also
        group = submission.group
        for member in group.members.all():
          Notification.objects.create(user=member, message=f"Your thesis submission for project \"{submission.project.title}\" has been approved.", link="/submissions")
        Notification.objects.create(user=group.creator, message=f"Your thesis submission for project \"{submission.project.title}\" has been approved.", link="/submissions")

      elif 'reject' in request.POST:
        submission.is_approved = False
        submission.save()
        group = submission.group
        for member in group.members.all():
          Notification.objects.create(user=member, message=f"Your thesis submission for project \"{submission.project.title}\" has been rejected.", link="/submissions")
        Notification.objects.create(user=group.creator, message=f"Your thesis submission for project \"{submission.project.title}\" has been rejected.", link="/submissions")

      return redirect('submissions')
  else:
    submissions = ThesisSubmit.objects.filter(
      Q(group__members=request.user) | Q(group__creator=request.user) | Q(project__supervisor__user=request.user)
    )
    return render(request, 'submissions.html', {'submissions': submissions})

@login_required
def setUserType(request):
    if request.method == 'POST':
        user = request.user
        user.user_type = request.POST['user_type']
        user.save()
        if (user.user_type == 'supervisor'):
          supervisors.objects.create(user=user)
        elif (user.user_type == 'unit_coordinator'):
          unitCoordinators.objects.create(user=user)

        return redirect('home')
    else:
        form = CustomUserCreationForm()
        return render(request, 'set_user_type.html',
            {'form': form}
        )