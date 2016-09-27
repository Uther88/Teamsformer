from .models import User
from django.shortcuts import HttpResponse
from functools import wraps
from .models import Team

def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs


# Decorators
def check_permission(view=None):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            team = Team.objects.get(pk=request.POST.get('team'))
            if request.user.pk is not team.admin.pk:
                return HttpResponse('It is not your team!')
            return view(request, *args, **kwargs)

        return wrapper

    return decorator(view) if view else decorator

