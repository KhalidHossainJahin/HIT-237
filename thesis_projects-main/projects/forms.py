# projects/forms.py
from django import forms
from django.forms import ModelForm
from customUser.models import CustomUser
from projects.models import ThesisSubmit, ProjectItem
from studentGroup.models import studentGroup, applyProject
from django.db.models import Q

class ProjectItemForm(ModelForm):
    class Meta:
        model = ProjectItem
        fields = ['title', 'supervisor', 'brief_description', 'full_description', 'topic_number']
        widgets = {
            'supervisor': forms.TextInput(attrs={'readonly': True}),
        }
class ThesisSubmitForm(ModelForm):
    class Meta:
        model = ThesisSubmit
        fields = ['group', 'project', 'file']

    def __init__(self, *args, **kwargs):
      user = kwargs.pop('user', None)
      super().__init__(*args, **kwargs)
      if user:
          self.fields['project'].queryset = ProjectItem.objects.filter(
              Q(applyproject__group__members=user) | Q(applyproject__group__creator=user),
              applyproject__is_approved=True,
              applyproject__is_rejected=False
          )