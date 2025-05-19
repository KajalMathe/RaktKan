from django.shortcuts import redirect

def recipient_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'recipient_id' not in request.session:
            return redirect('recipient_login')
        return view_func(request, *args, **kwargs)
    return wrapper
