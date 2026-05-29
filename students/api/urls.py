"""API URL configuration using DRF Router."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import (
    AttendanceViewSet,
    ClassInfoViewSet,
    CourseViewSet,
    DepartmentViewSet,
    EnrollmentViewSet,
    StudentViewSet,
    TeacherViewSet,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"classes", ClassInfoViewSet)
router.register(r"teachers", TeacherViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"students", StudentViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"attendances", AttendanceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
