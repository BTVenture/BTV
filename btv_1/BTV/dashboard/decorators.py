from functools import wraps
from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required as django_login_required

def login_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login')
        return view_function(request, *args, **kwargs)
    return wrapper

# Now, you can use login_required decorator instead of django.contrib.auth.decorators.login_required
# login_required = django_login_required(login_required)
