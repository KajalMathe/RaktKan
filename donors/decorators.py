from django.shortcuts import redirect

def donor_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'donor_id' not in request.session:
            return redirect('donor_login')
        return view_func(request, *args, **kwargs)
    return wrapper
