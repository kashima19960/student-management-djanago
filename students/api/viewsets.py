"""DRF ViewSets for all models."""

from django.db.models import Avg, Count, Max, Min
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from students.models import (
    Attendance,
    ClassInfo,
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
)

from .serializers import (
    AttendanceSerializer,
    ClassInfoSerializer,
    CourseSerializer,
    DepartmentSerializer,
    EnrollmentSerializer,
    StudentSerializer,
    TeacherSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ["name", "code"]


class ClassInfoViewSet(viewsets.ModelViewSet):
    queryset = ClassInfo.objects.select_related("department").all()
    serializer_class = ClassInfoSerializer
    filterset_fields = ["department", "grade_year"]
    search_fields = ["name"]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related("department").all()
    serializer_class = TeacherSerializer
    filterset_fields = ["department"]
    search_fields = ["teacher_id", "name"]

    @action(detail=True, methods=["get"])
    def courses(self, request, pk=None):
        teacher = self.get_object()
        courses = teacher.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("teacher", "department").all()
    serializer_class = CourseSerializer
    filterset_fields = ["department", "teacher"]
    search_fields = ["course_id", "name"]

    @action(detail=True, methods=["get"])
    def enrollments(self, request, pk=None):
        course = self.get_object()
        enrollments = course.enrollments.select_related("student").all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        course = self.get_object()
        enrollments = course.enrollments.filter(score__isnull=False)
        stats = enrollments.aggregate(
            avg=Avg("score"), max_score=Max("score"), min_score=Min("score"), count=Count("id")
        )
        pass_count = enrollments.filter(score__gte=60).count()
        total = stats["count"] or 0
        return Response({
            **stats,
            "pass_count": pass_count,
            "pass_rate": round(pass_count / total * 100, 1) if total > 0 else 0,
        })


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("class_info").all()
    serializer_class = StudentSerializer
    filterset_fields = ["major", "class_info"]
    search_fields = ["student_id", "name", "major"]

    @action(detail=True, methods=["get"])
    def enrollments(self, request, pk=None):
        student = self.get_object()
        enrollments = student.enrollments.select_related("course").all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def attendances(self, request, pk=None):
        student = self.get_object()
        records = student.attendances.select_related("course").all()
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related("student", "course").all()
    serializer_class = EnrollmentSerializer
    filterset_fields = ["student", "course", "semester", "status"]
    search_fields = ["student__name", "student__student_id"]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("student", "course").all()
    serializer_class = AttendanceSerializer
    filterset_fields = ["student", "course", "date", "status"]
    search_fields = ["student__name", "student__student_id"]
