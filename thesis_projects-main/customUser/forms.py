from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type']
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].required = True

    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.user_type = self.cleaned_data['user_type']
        user.save()
        return user