from .models import studentGroup, applyProject
from django import forms

class applyProjectForm(forms.ModelForm):
    class Meta:
        model = applyProject
        fields = ['project', 'cv_zip_link']
        widgets = {
          'project': forms.Select(attrs={'readonly': True}),
        }