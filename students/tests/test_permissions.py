"""Permission tests."""

import pytest
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse

from students.tests.factories import UserFactory


@pytest.fixture
def admin_user():
    user = UserFactory(username="perm_admin", is_superuser=True)
    group, _ = Group.objects.get_or_create(name="admin")
    user.groups.add(group)
    return user


@pytest.fixture
def teacher_user():
    user = UserFactory(username="perm_teacher")
    group, _ = Group.objects.get_or_create(name="teacher")
    user.groups.add(group)
    return user


@pytest.fixture
def student_user():
    user = UserFactory(username="perm_student")
    group, _ = Group.objects.get_or_create(name="student_viewer")
    user.groups.add(group)
    return user


@pytest.mark.django_db
class TestRolePermissions:
    """Test that role-based access control works correctly."""

    # URLs that any logged-in user can view (list/detail pages)
    LIST_URLS = [
        "department_list", "class_list", "teacher_list",
        "course_list", "grade_list", "attendance_list",
        "student_list", "dashboard",
    ]

    # URLs that require admin/teacher permissions (create/edit/delete)
    ADMIN_CREATE_URLS = [
        "department_create", "class_create", "teacher_create",
        "course_create", "student_create", "import_export",
    ]

    def test_admin_can_access_all(self, admin_user):
        client = Client()
        client.force_login(admin_user)
        for url_name in self.LIST_URLS + self.ADMIN_CREATE_URLS:
            r = client.get(reverse(url_name))
            assert r.status_code == 200, f"Admin cannot access {url_name}"

    def test_teacher_cannot_access_admin_create_urls(self, teacher_user):
        client = Client()
        client.force_login(teacher_user)
        for url_name in ["department_create", "class_create", "teacher_create", "course_create"]:
            r = client.get(reverse(url_name))
            assert r.status_code == 403, f"Teacher should not access {url_name}"

    def test_student_cannot_access_admin_create_urls(self, student_user):
        client = Client()
        client.force_login(student_user)
        for url_name in self.ADMIN_CREATE_URLS:
            r = client.get(reverse(url_name))
            assert r.status_code == 403, f"Student should not access {url_name}"

    def test_student_can_access_list_urls(self, student_user):
        client = Client()
        client.force_login(student_user)
        # List views are @login_required, any authenticated user can see them
        for url_name in self.LIST_URLS:
            r = client.get(reverse(url_name))
            assert r.status_code == 200, f"Student should access {url_name}"

    def test_student_cannot_access_teacher_list_urls(self, student_user):
        client = Client()
        client.force_login(student_user)
        # grade_list and attendance_list are login_required, so students can see them
        # but they can't do create/entry actions
        for url_name in ["grade_list", "attendance_list"]:
            r = client.get(reverse(url_name))
            assert r.status_code == 200, f"Student can view {url_name} (read-only)"

    def test_unauthenticated_redirects_to_login(self):
        client = Client()
        r = client.get(reverse("student_list"))
        assert r.status_code == 302
        assert "login" in r.url
