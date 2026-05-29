from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Attendance,
    AuditLog,
    ClassInfo,
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "created_at")
    search_fields = ("name", "code")


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "grade_year", "advisor")
    list_filter = ("department", "grade_year")
    search_fields = ("name",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("teacher_id", "name", "department", "phone", "email")
    list_filter = ("department",)
    search_fields = ("teacher_id", "name")


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    list_display = ("student_id", "name", "age", "major", "class_info", "enrollment_date", "graduation_date")
    list_filter = ("major", "class_info__department")
    search_fields = ("student_id", "name", "major")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_id", "name", "credit", "teacher", "department", "max_students")
    list_filter = ("department", "teacher")
    search_fields = ("course_id", "name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "score", "grade_point", "status", "enrolled_at")
    list_filter = ("semester", "status", "course__department")
    search_fields = ("student__name", "student__student_id", "course__name")
    readonly_fields = ("grade_point",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "status", "remark")
    list_filter = ("date", "status", "course")
    search_fields = ("student__name", "student__student_id")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "model_name", "object_id", "ip_address")
    list_filter = ("action", "model_name", "timestamp")
    search_fields = ("object_repr", "model_name")
    readonly_fields = ("user", "action", "model_name", "object_id", "object_repr", "changes", "ip_address", "timestamp")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
