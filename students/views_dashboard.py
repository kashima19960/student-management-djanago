"""Dashboard views with Chart.js data endpoints."""

import json

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import Attendance, Course, Enrollment, Student, Teacher


@login_required
def dashboard(request):
    """Main dashboard page."""
    stats = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_teachers": Teacher.objects.count(),
    }
    return render(request, "dashboard.html", {"stats": stats})


@login_required
def dashboard_api_stats(request):
    """API endpoint: basic counts."""
    return JsonResponse({
        "students": Student.objects.count(),
        "courses": Course.objects.count(),
        "teachers": Teacher.objects.count(),
    })


@login_required
def dashboard_api_major_distribution(request):
    """API endpoint: student count by major."""
    data = (
        Student.objects.values("major")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return JsonResponse({
        "labels": [d["major"] for d in data],
        "values": [d["count"] for d in data],
    })


@login_required
def dashboard_api_age_distribution(request):
    """API endpoint: student age distribution."""
    data = (
        Student.objects.values("age")
        .annotate(count=Count("id"))
        .order_by("age")
    )
    return JsonResponse({
        "labels": [str(d["age"]) for d in data],
        "values": [d["count"] for d in data],
    })


@login_required
def dashboard_api_enrollment_trend(request):
    """API endpoint: enrollment by grade year."""
    from django.db.models.functions import ExtractYear

    data = (
        Student.objects.values("enrollment_date__year")
        .annotate(count=Count("id"))
        .order_by("enrollment_date__year")
    )
    return JsonResponse({
        "labels": [str(d["enrollment_date__year"]) for d in data],
        "values": [d["count"] for d in data],
    })


@login_required
def dashboard_api_gpa_distribution(request):
    """API endpoint: GPA distribution."""
    bins = {"4.0": 0, "3.0-3.9": 0, "2.0-2.9": 0, "1.0-1.9": 0, "0-0.9": 0}
    for e in Enrollment.objects.filter(grade_point__isnull=False):
        gp = float(e.grade_point)
        if gp >= 4.0:
            bins["4.0"] += 1
        elif gp >= 3.0:
            bins["3.0-3.9"] += 1
        elif gp >= 2.0:
            bins["2.0-2.9"] += 1
        elif gp >= 1.0:
            bins["1.0-1.9"] += 1
        else:
            bins["0-0.9"] += 1
    return JsonResponse({"labels": list(bins.keys()), "values": list(bins.values())})


@login_required
def dashboard_api_attendance_rate(request):
    """API endpoint: attendance rate per course."""
    courses = Course.objects.all()
    labels, values = [], []
    for course in courses:
        total = course.attendances.count()
        if total > 0:
            present = course.attendances.filter(status="present").count()
            rate = round(present / total * 100, 1)
        else:
            rate = 0
        labels.append(course.name)
        values.append(rate)
    return JsonResponse({"labels": labels, "values": values})
