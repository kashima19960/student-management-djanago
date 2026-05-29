"""Grade management views."""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .models import Course, Enrollment, Student
from .utils import paginate_queryset


@login_required
def grade_list(request):
    """List all enrollments with grades, filterable by student or course."""
    query = (request.GET.get("q") or "").strip()
    course_id = request.GET.get("course", "")
    enrollments = Enrollment.objects.select_related("student", "course").all()
    if query:
        enrollments = enrollments.filter(
            Q(student__name__icontains=query) | Q(student__student_id__icontains=query)
        )
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
    courses = Course.objects.all()
    page_obj = paginate_queryset(enrollments, request)
    return render(request, "grade_list.html", {
        "page_obj": page_obj,
        "enrollments": page_obj.object_list,
        "query": query,
        "courses": courses,
        "selected_course": course_id,
    })


@permission_required_custom("students.can_manage_grade")
def grade_entry(request, course_pk):
    """Batch entry of grades for a course."""
    course = get_object_or_404(Course, pk=course_pk)
    enrollments = course.enrollments.select_related("student").all()

    if request.method == "POST":
        for enrollment in enrollments:
            score_key = f"score_{enrollment.pk}"
            score_str = request.POST.get(score_key, "").strip()
            if score_str:
                try:
                    score = Decimal(score_str)
                    if 0 <= score <= 100:
                        enrollment.score = score
                        enrollment.status = "completed"
                        enrollment.save()
                except Exception:
                    pass
        messages.success(request, f"《{course.name}》成绩已保存")
        return redirect("grade_list")

    return render(request, "grade_entry.html", {
        "course": course,
        "enrollments": enrollments,
    })


@login_required
def grade_statistics(request, course_pk):
    """Show grade statistics for a course."""
    course = get_object_or_404(Course, pk=course_pk)
    enrollments = course.enrollments.filter(score__isnull=False)

    stats = enrollments.aggregate(
        avg_score=Avg("score"),
        max_score=Max("score"),
        min_score=Min("score"),
        count=Count("id"),
    )
    pass_count = enrollments.filter(score__gte=60).count()
    total = stats["count"] or 0
    pass_rate = (pass_count / total * 100) if total > 0 else 0

    # GPA distribution
    gpa_4 = enrollments.filter(grade_point__gte=4).count()
    gpa_3 = enrollments.filter(grade_point__gte=3, grade_point__lt=4).count()
    gpa_2 = enrollments.filter(grade_point__gte=2, grade_point__lt=3).count()
    gpa_1 = enrollments.filter(grade_point__gte=1, grade_point__lt=2).count()
    gpa_0 = enrollments.filter(grade_point__lt=1).count()
    import json
    gpa_values_json = json.dumps([gpa_4, gpa_3, gpa_2, gpa_1, gpa_0])

    return render(request, "grade_statistics.html", {
        "course": course,
        "stats": stats,
        "pass_rate": round(pass_rate, 1),
        "total": total,
        "gpa_4": gpa_4,
        "gpa_3": gpa_3,
        "gpa_2": gpa_2,
        "gpa_1": gpa_1,
        "gpa_0": gpa_0,
        "gpa_values_json": gpa_values_json,
    })
