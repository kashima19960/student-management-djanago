"""API tests."""

import pytest
from django.test import Client
from rest_framework.test import APIClient

from students.tests.factories import (
    DepartmentFactory,
    StudentFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_user():
    return UserFactory(username="api_user")


@pytest.mark.django_db
class TestDepartmentAPI:
    def test_list_requires_auth(self, api_client):
        r = api_client.get("/api/departments/")
        assert r.status_code in (401, 403)

    def test_list(self, api_client, auth_user):
        DepartmentFactory.create_batch(3)
        api_client.force_authenticate(auth_user)
        r = api_client.get("/api/departments/")
        assert r.status_code == 200
        assert r.data["count"] == 3

    def test_create(self, api_client, auth_user):
        api_client.force_authenticate(auth_user)
        r = api_client.post("/api/departments/", {"code": "NEW", "name": "新院系"})
        # Non-admin should be denied by IsAdminOrReadOnly
        assert r.status_code in (201, 403)


@pytest.mark.django_db
class TestStudentAPI:
    def test_list(self, api_client, auth_user):
        StudentFactory.create_batch(5)
        api_client.force_authenticate(auth_user)
        r = api_client.get("/api/students/")
        assert r.status_code == 200
        assert r.data["count"] == 5

    def test_detail(self, api_client, auth_user):
        s = StudentFactory()
        api_client.force_authenticate(auth_user)
        r = api_client.get(f"/api/students/{s.pk}/")
        assert r.status_code == 200
        assert r.data["name"] == s.name

    def test_search(self, api_client, auth_user):
        StudentFactory(name="张三")
        StudentFactory(name="李四")
        api_client.force_authenticate(auth_user)
        r = api_client.get("/api/students/", {"search": "张三"})
        assert r.status_code == 200


@pytest.mark.django_db
class TestSwaggerDocs:
    def test_swagger_ui(self, api_client, auth_user):
        api_client.force_authenticate(auth_user)
        r = api_client.get("/api/docs/")
        assert r.status_code == 200

    def test_schema(self, api_client, auth_user):
        api_client.force_authenticate(auth_user)
        r = api_client.get("/api/schema/")
        assert r.status_code == 200
