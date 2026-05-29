"""Model tests."""

import pytest
from django.core.exceptions import ValidationError

from students.models import Enrollment
from students.tests.factories import (
    AttendanceFactory,
    CourseFactory,
    DepartmentFactory,
    EnrollmentFactory,
    StudentFactory,
    TeacherFactory,
)


@pytest.mark.django_db
class TestDepartment:
    def test_create(self):
        dept = DepartmentFactory(code="CS", name="计算机学院")
        assert str(dept) == "CS - 计算机学院"
        assert dept.pk is not None

    def test_unique_code(self):
        from students.models import Department
        DepartmentFactory(code="CS")
        with pytest.raises(Exception):
            Department.objects.create(code="CS", name="重复")


@pytest.mark.django_db
class TestStudent:
    def test_create(self):
        s = StudentFactory(name="张三")
        assert "张三" in str(s)

    def test_student_id_unique(self):
        from students.models import Student
        StudentFactory(student_id="2024000001")
        with pytest.raises(Exception):
            Student.objects.create(student_id="2024000001", name="重复", age=20, major="CS", enrollment_date="2024-09-01", graduation_date="2028-06-30")


@pytest.mark.django_db
class TestEnrollment:
    def test_grade_point_auto_calc(self):
        e = EnrollmentFactory(score=95)
        assert float(e.grade_point) == 4.0

        e.score = 85
        e.save()
        assert float(e.grade_point) == 3.0

        e.score = 75
        e.save()
        assert float(e.grade_point) == 2.0

        e.score = 65
        e.save()
        assert float(e.grade_point) == 1.0

        e.score = 50
        e.save()
        assert float(e.grade_point) == 0.0

    def test_unique_constraint(self):
        s = StudentFactory()
        c = CourseFactory()
        EnrollmentFactory(student=s, course=c, semester="2024-1")
        with pytest.raises(Exception):
            EnrollmentFactory(student=s, course=c, semester="2024-1")


@pytest.mark.django_db
class TestAttendance:
    def test_create(self):
        a = AttendanceFactory(status="late")
        assert "迟到" in str(a)


@pytest.mark.django_db
class TestTeacher:
    def test_create(self):
        t = TeacherFactory(name="李老师")
        assert "李老师" in str(t)


@pytest.mark.django_db
class TestCourse:
    def test_create(self):
        c = CourseFactory(name="Python编程", credit=4)
        assert "Python编程" in str(c)
        assert c.credit == 4
