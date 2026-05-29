"""Form tests."""

import pytest
from django.contrib.auth.models import Group

from students.forms import RegisterForm, StudentForm
from students.tests.factories import DepartmentFactory


@pytest.mark.django_db
class TestStudentForm:
    def test_valid_form(self):
        dept = DepartmentFactory()
        data = {
            "student_id": "2024000001",
            "name": "张三",
            "age": 20,
            "major": "CS",
            "enrollment_date": "2024-09-01",
            "graduation_date": "2028-06-30",
        }
        form = StudentForm(data=data)
        assert form.is_valid()

    def test_enrollment_after_graduation(self):
        data = {
            "student_id": "2024000001",
            "name": "张三",
            "age": 20,
            "major": "CS",
            "enrollment_date": "2028-09-01",
            "graduation_date": "2024-06-30",
        }
        form = StudentForm(data=data)
        assert not form.is_valid()

    def test_missing_required_fields(self):
        form = StudentForm(data={})
        assert not form.is_valid()
        assert "student_id" in form.errors
        assert "name" in form.errors


@pytest.mark.django_db
class TestRegisterForm:
    def test_register_creates_user_with_role(self):
        Group.objects.get_or_create(name="student_viewer")
        data = {
            "username": "newuser",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = RegisterForm(data=data)
        assert form.is_valid()
        user = form.save()
        assert user.groups.filter(name="student_viewer").exists()
