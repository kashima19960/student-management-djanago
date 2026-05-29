"""Test factories using factory_boy."""

import factory
from django.contrib.auth.models import Group, User
from students.models import (
    Attendance,
    ClassInfo,
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
)


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department
        django_get_or_create = ("code",)

    code = factory.Sequence(lambda n: f"DEPT{n:03d}")
    name = factory.Sequence(lambda n: f"院系{n}")


class ClassInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClassInfo

    name = factory.Sequence(lambda n: f"班级{n:03d}")
    department = factory.SubFactory(DepartmentFactory)
    grade_year = 2024
    advisor = "张老师"


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher
        django_get_or_create = ("teacher_id",)

    teacher_id = factory.Sequence(lambda n: f"T{n:06d}")
    name = factory.Sequence(lambda n: f"教师{n}")
    department = factory.SubFactory(DepartmentFactory)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
        django_get_or_create = ("student_id",)

    student_id = factory.Sequence(lambda n: f"{2024000000 + n}")
    name = factory.Sequence(lambda n: f"学生{n}")
    age = 20
    major = "计算机科学"
    enrollment_date = "2024-09-01"
    graduation_date = "2028-06-30"
    class_info = factory.SubFactory(ClassInfoFactory)


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ("course_id",)

    course_id = factory.Sequence(lambda n: f"CS{n:04d}")
    name = factory.Sequence(lambda n: f"课程{n}")
    credit = 3
    teacher = factory.SubFactory(TeacherFactory)
    department = factory.SubFactory(DepartmentFactory)


class EnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment

    student = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)
    semester = "2024-2025-1"


class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance

    student = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)
    date = "2024-10-01"
    status = "present"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
