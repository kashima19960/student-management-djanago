"""Custom decorators for role-based access control."""

from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decorator that checks whether the user belongs to one of the given groups.

    Usage:
        @role_required("admin", "teacher")
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            user_groups = set(request.user.groups.values_list("name", flat=True))
            if not user_groups.intersection(roles):
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": "权限不足"}, status=403)
                raise PermissionDenied("您没有权限访问此页面")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def permission_required_custom(perm):
    """
    Enhanced permission_required that returns JSON 403 for AJAX requests.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if not request.user.has_perm(perm):
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": "权限不足"}, status=403)
                raise PermissionDenied("您没有权限执行此操作")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
