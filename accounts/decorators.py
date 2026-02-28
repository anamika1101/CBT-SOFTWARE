from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import Role


def require_role(required_role):
    """
    Decorator to ensure a user has the correct role.
    - If session is not for the required role, redirects to homepage
    - Usage: @require_role('company') for company views, etc.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if required_role.lower() == 'company':
                if not request.session.get('com_id'):
                    messages.warning(request, 'Please login as Company first.')
                    return redirect('homepage')
                    
            elif required_role.lower() == 'center':
                if not request.session.get('center_id'):
                    messages.warning(request, 'Please login as Center first.')
                    return redirect('homepage')
                    
            elif required_role.lower() == 'admin':
                if not request.session.get('admin_id'):
                    messages.warning(request, 'Please login as Admin first.')
                    return redirect('homepage')
                    
            else:
                return redirect('homepage')
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def logout_user(request):
    """
    Clear all session data
    """
    for key in list(request.session.keys()):
        del request.session[key]
    return True
