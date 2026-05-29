"""Mixins for role-based access control in class-based views."""

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect


class RoleRequiredMixin:
    """
    CBV mixin that restricts access to users in specific groups.

    Set ``allowed_roles`` on the view class:
        class MyView(RoleRequiredMixin, View):
            allowed_roles = ["admin", "teacher"]
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        user_groups = set(request.user.groups.values_list("name", flat=True))
        if not user_groups.intersection(self.allowed_roles):
            raise PermissionDenied("您没有权限访问此页面")
        return super().dispatch(request, *args, **kwargs)


class PermissionRequiredMixin:
    """
    CBV mixin that checks a single Django permission.

    Set ``permission_required`` on the view class:
        class MyView(PermissionRequiredMixin, View):
            permission_required = "students.can_manage_student"
    """
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if self.permission_required and not request.user.has_perm(self.permission_required):
            raise PermissionDenied("您没有权限执行此操作")
        return super().dispatch(request, *args, **kwargs)
