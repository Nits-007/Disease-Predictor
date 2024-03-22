from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Redirect to the home page if the user is already authenticated
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
