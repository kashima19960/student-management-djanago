"""Attendance management views."""

from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .models import Attendance, Course, Student
from .utils import paginate_queryset


@login_required
def attendance_list(request):
    """List attendance records with filters."""
    query = (request.GET.get("q") or "").strip()
    course_id = request.GET.get("course", "")
    records = Attendance.objects.select_related("student", "course").all()
    if query:
        records = records.filter(
            Q(student__name__icontains=query) | Q(student__student_id__icontains=query)
        )
    if course_id:
        records = records.filter(course_id=course_id)
    courses = Course.objects.all()
    page_obj = paginate_queryset(records, request)
    return render(request, "attendance_list.html", {
        "page_obj": page_obj,
        "records": page_obj.object_list,
        "query": query,
        "courses": courses,
        "selected_course": course_id,
    })


@permission_required_custom("students.can_manage_attendance")
def attendance_entry(request, course_pk):
    """Batch attendance entry for a course on a given date."""
    course = get_object_or_404(Course, pk=course_pk)
    entry_date = request.GET.get("date") or request.POST.get("date") or str(date.today())
    enrollments = course.enrollments.select_related("student").all()

    if request.method == "POST":
        created_count = 0
        for enrollment in enrollments:
            status_key = f"status_{enrollment.student.pk}"
            remark_key = f"remark_{enrollment.student.pk}"
            status = request.POST.get(status_key, "present")
            remark = request.POST.get(remark_key, "")
            obj, created = Attendance.objects.update_or_create(
                student=enrollment.student,
                course=course,
                date=entry_date,
                defaults={"status": status, "remark": remark},
            )
            if created:
                created_count += 1
        messages.success(request, f"已记录 {created_count} 条考勤（{entry_date}）")
        return redirect("attendance_list")

    # Pre-load existing attendance for this date
    existing = Attendance.objects.filter(course=course, date=entry_date)
    existing_map = {a.student_id: a for a in existing}

    return render(request, "attendance_entry.html", {
        "course": course,
        "enrollments": enrollments,
        "entry_date": entry_date,
        "existing_map": existing_map,
    })


@login_required
def attendance_statistics(request, course_pk):
    """Show attendance statistics for a course."""
    course = get_object_or_404(Course, pk=course_pk)
    records = course.attendances.all()
    total = records.count()

    status_counts = records.values("status").annotate(count=Count("id"))
    status_map = {item["status"]: item["count"] for item in status_counts}

    present = status_map.get("present", 0)
    late = status_map.get("late", 0)
    absent = status_map.get("absent", 0)
    leave = status_map.get("leave", 0)

    attendance_rate = ((present + late) / total * 100) if total > 0 else 0

    return render(request, "attendance_statistics.html", {
        "course": course,
        "total": total,
        "present": present,
        "late": late,
        "absent": absent,
        "leave": leave,
        "attendance_rate": round(attendance_rate, 1),
    })
