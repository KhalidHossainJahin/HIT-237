from .models import studentGroup
from django.http import HttpResponse
from django.db.models import Q

def user_groups(request):
    if request.user.is_authenticated:
        is_member = studentGroup.objects.filter(members=request.user).exists()
        is_creator = studentGroup.objects.filter(creator=request.user).exists()
        if (is_member or is_creator):
            # member creator both
            group = studentGroup.objects.filter(Q(members=request.user) | Q(creator=request.user)).first()
            if group is not None:
                group_id = group.id
                return {'group_id': group_id}
            else:
              print("No group found")
              return {}
        else:
            return {}
    else:
        return {}

def user_type(request):
    if request.user.is_authenticated:
      user_type = request.user.user_type
      if user_type is not None:
        return {'user_type': user_type}
      else:
        return {}
    else:
        return {}