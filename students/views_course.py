"""Course CRUD views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .forms import CourseForm
from .models import Course
from .utils import paginate_queryset


@login_required
def course_list(request):
    query = (request.GET.get("q") or "").strip()
    courses = Course.objects.select_related("teacher", "department").all()
    if query:
        courses = courses.filter(
            Q(course_id__icontains=query) | Q(name__icontains=query)
        )
    page_obj = paginate_queryset(courses, request)
    return render(request, "course_list.html", {
        "page_obj": page_obj,
        "courses": page_obj.object_list,
        "query": query,
    })


@permission_required_custom("students.can_manage_course")
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "课程已创建")
            return redirect("course_list")
    else:
        form = CourseForm()
    return render(request, "course_form.html", {"form": form, "mode": "create"})


@permission_required_custom("students.can_manage_course")
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "课程已更新")
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)
    return render(request, "course_form.html", {"form": form, "mode": "update", "course": course})


@permission_required_custom("students.can_manage_course")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        messages.success(request, "课程已删除")
    return redirect("course_list")


@login_required
def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related("teacher", "department"), pk=pk
    )
    enrollments = course.enrollments.select_related("student").all()
    return render(request, "course_detail.html", {
        "course": course,
        "enrollments": enrollments,
    })
