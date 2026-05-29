"""View tests."""

import pytest
from django.test import Client
from django.urls import reverse

from students.tests.factories import (
    CourseFactory,
    DepartmentFactory,
    StudentFactory,
    UserFactory,
)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_user():
    from django.contrib.auth.models import Group

    user = UserFactory(username="admin_test", is_superuser=True)
    group, _ = Group.objects.get_or_create(name="admin")
    user.groups.add(group)
    return user


@pytest.fixture
def student_user():
    from django.contrib.auth.models import Group

    user = UserFactory(username="student_test")
    group, _ = Group.objects.get_or_create(name="student_viewer")
    user.groups.add(group)
    return user


@pytest.mark.django_db
class TestAuthViews:
    def test_login_page(self, client):
        r = client.get(reverse("login"))
        assert r.status_code == 200

    def test_register_page(self, client):
        r = client.get(reverse("register"))
        assert r.status_code == 200

    def test_login_redirect(self, client):
        r = client.get("/")
        assert r.status_code == 302

    def test_login_success(self, client):
        UserFactory(username="testuser", password="testpass123")
        r = client.post(reverse("login"), {"username": "testuser", "password": "testpass123"})
        assert r.status_code == 302


@pytest.mark.django_db
class TestStudentViews:
    def test_student_list_requires_login(self, client):
        r = client.get(reverse("student_list"))
        assert r.status_code == 302

    def test_student_list(self, client, admin_user):
        StudentFactory.create_batch(5)
        client.force_login(admin_user)
        r = client.get(reverse("student_list"))
        assert r.status_code == 200
        assert len(r.context["students"]) == 5

    def test_student_list_pagination(self, client, admin_user):
        StudentFactory.create_batch(20)
        client.force_login(admin_user)
        r = client.get(reverse("student_list"))
        assert r.status_code == 200
        assert len(r.context["students"]) == 15

    def test_student_search(self, client, admin_user):
        StudentFactory(name="张三")
        StudentFactory(name="李四")
        client.force_login(admin_user)
        r = client.get(reverse("student_list"), {"q": "张三"})
        assert r.status_code == 200
        assert len(r.context["students"]) == 1

    def test_student_create_requires_admin(self, client, student_user):
        client.force_login(student_user)
        r = client.get(reverse("student_create"))
        assert r.status_code == 403

    def test_student_create(self, client, admin_user):
        dept = DepartmentFactory()
        client.force_login(admin_user)
        data = {
            "student_id": "2024000999",
            "name": "新学生",
            "age": 20,
            "major": "CS",
            "enrollment_date": "2024-09-01",
            "graduation_date": "2028-06-30",
        }
        r = client.post(reverse("student_create"), data)
        assert r.status_code == 302

    def test_student_delete(self, client, admin_user):
        s = StudentFactory()
        client.force_login(admin_user)
        r = client.post(reverse("student_delete", args=[s.pk]))
        assert r.status_code == 302


@pytest.mark.django_db
class TestDashboardViews:
    def test_dashboard(self, client, admin_user):
        client.force_login(admin_user)
        r = client.get(reverse("dashboard"))
        assert r.status_code == 200
        assert "total_students" in r.context["stats"]

    def test_dashboard_api(self, client, admin_user):
        StudentFactory.create_batch(3)
        client.force_login(admin_user)
        r = client.get(reverse("dashboard_api_stats"))
        assert r.status_code == 200
        data = r.json()
        assert data["students"] == 3


@pytest.mark.django_db
class TestPermissionViews:
    def test_admin_can_access_all(self, client, admin_user):
        client.force_login(admin_user)
        for url_name in ["department_list", "teacher_list", "course_list", "grade_list", "attendance_list"]:
            r = client.get(reverse(url_name))
            assert r.status_code == 200, f"{url_name} failed"

    def test_student_cannot_access_create_urls(self, client, student_user):
        client.force_login(student_user)
        for url_name in ["student_create", "department_create", "teacher_create"]:
            r = client.get(reverse(url_name))
            assert r.status_code == 403, f"{url_name} should be 403 for student"
