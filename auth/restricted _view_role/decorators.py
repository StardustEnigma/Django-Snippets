from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden

# ✅ Decorator to restrict access based on login and user role
def login_and_role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required  # Ensure the user is logged in
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            # 🔒 If required role is 'applicant' but user is not an applicant
            if required_role == "applicant" and not user.is_applicant:
                return HttpResponseForbidden(error_303_html)

            # 🔒 If required role is 'recruiter' but user is not a recruiter
            if required_role == "recruiter" and not user.is_recruiter:
                return HttpResponseForbidden(error_303_html)

            # ✅ All checks passed, proceed to view
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
# in the app named core

@login_and_role_required("recruiter")
def recruiter_dashboard(request):
    # ... will be use
    ...