"""Custom template tags for role and permission checks."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_role(context, *roles):
    """
    Check if the current user belongs to any of the given groups.

    Usage:
        {% has_role "admin" "teacher" as is_manager %}
        {% if is_manager %}...{% endif %}
    """
    request = context.get("request")
    if request and request.user.is_authenticated:
        user_groups = set(request.user.groups.values_list("name", flat=True))
        return bool(user_groups.intersection(roles))
    return False


@register.simple_tag(takes_context=True)
def has_perm(context, perm):
    """
    Check if the current user has a specific permission.

    Usage:
        {% has_perm "students.can_manage_student" as can_manage %}
        {% if can_manage %}...{% endif %}
    """
    request = context.get("request")
    if request and request.user.is_authenticated:
        return request.user.has_perm(perm)
    return False


@register.filter
def has_group(user, group_name):
    """
    Template filter to check user group membership.

    Usage:
        {% if user|has_group:"admin" %}...{% endif %}
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False
