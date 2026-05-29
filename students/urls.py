from django.urls import path

from . import views
from .views_attendance import (
    attendance_entry,
    attendance_list,
    attendance_statistics,
)
from .views_class import (
    class_create,
    class_delete,
    class_detail,
    class_list,
    class_update,
)
from .views_course import (
    course_create,
    course_delete,
    course_detail,
    course_list,
    course_update,
)
from .views_dashboard import (
    dashboard,
    dashboard_api_age_distribution,
    dashboard_api_attendance_rate,
    dashboard_api_enrollment_trend,
    dashboard_api_gpa_distribution,
    dashboard_api_major_distribution,
    dashboard_api_stats,
)
from .views_department import (
    department_create,
    department_delete,
    department_list,
    department_update,
)
from .views_grade import grade_entry, grade_list, grade_statistics
from .views_import_export import export_students, import_export
from .views_report import student_report_pdf
from .views_teacher import (
    teacher_create,
    teacher_delete,
    teacher_detail,
    teacher_list,
    teacher_update,
)

urlpatterns = [
    # Auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    # Dashboard
    path("", dashboard, name="dashboard"),
    path("dashboard/api/stats/", dashboard_api_stats, name="dashboard_api_stats"),
    path("dashboard/api/major-distribution/", dashboard_api_major_distribution, name="dashboard_api_major_distribution"),
    path("dashboard/api/age-distribution/", dashboard_api_age_distribution, name="dashboard_api_age_distribution"),
    path("dashboard/api/enrollment-trend/", dashboard_api_enrollment_trend, name="dashboard_api_enrollment_trend"),
    path("dashboard/api/gpa-distribution/", dashboard_api_gpa_distribution, name="dashboard_api_gpa_distribution"),
    path("dashboard/api/attendance-rate/", dashboard_api_attendance_rate, name="dashboard_api_attendance_rate"),

    # Students
    path("students/", views.student_list, name="student_list"),
    path("students/new/", views.student_create, name="student_create"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("students/<int:pk>/report/", student_report_pdf, name="student_report_pdf"),

    # Departments
    path("departments/", department_list, name="department_list"),
    path("departments/new/", department_create, name="department_create"),
    path("departments/<int:pk>/edit/", department_update, name="department_update"),
    path("departments/<int:pk>/delete/", department_delete, name="department_delete"),

    # Classes
    path("classes/", class_list, name="class_list"),
    path("classes/new/", class_create, name="class_create"),
    path("classes/<int:pk>/edit/", class_update, name="class_update"),
    path("classes/<int:pk>/delete/", class_delete, name="class_delete"),
    path("classes/<int:pk>/", class_detail, name="class_detail"),

    # Teachers
    path("teachers/", teacher_list, name="teacher_list"),
    path("teachers/new/", teacher_create, name="teacher_create"),
    path("teachers/<int:pk>/edit/", teacher_update, name="teacher_update"),
    path("teachers/<int:pk>/delete/", teacher_delete, name="teacher_delete"),
    path("teachers/<int:pk>/", teacher_detail, name="teacher_detail"),

    # Courses
    path("courses/", course_list, name="course_list"),
    path("courses/new/", course_create, name="course_create"),
    path("courses/<int:pk>/edit/", course_update, name="course_update"),
    path("courses/<int:pk>/delete/", course_delete, name="course_delete"),
    path("courses/<int:pk>/", course_detail, name="course_detail"),

    # Grades
    path("grades/", grade_list, name="grade_list"),
    path("grades/course/<int:course_pk>/entry/", grade_entry, name="grade_entry"),
    path("grades/course/<int:course_pk>/statistics/", grade_statistics, name="grade_statistics"),

    # Attendance
    path("attendance/", attendance_list, name="attendance_list"),
    path("attendance/course/<int:course_pk>/entry/", attendance_entry, name="attendance_entry"),
    path("attendance/course/<int:course_pk>/statistics/", attendance_statistics, name="attendance_statistics"),

    # Import/Export
    path("import-export/", import_export, name="import_export"),
    path("export/students/", export_students, name="export_students"),
]
