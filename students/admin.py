from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "age", "major", "enrollment_date", "graduation_date")
    search_fields = ("student_id", "name", "major")
