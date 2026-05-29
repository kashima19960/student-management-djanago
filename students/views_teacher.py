"""Teacher CRUD views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .forms import TeacherForm
from .models import Teacher
from .utils import paginate_queryset


@login_required
def teacher_list(request):
    query = (request.GET.get("q") or "").strip()
    teachers = Teacher.objects.select_related("department").all()
    if query:
        teachers = teachers.filter(Q(teacher_id__icontains=query) | Q(name__icontains=query))
    page_obj = paginate_queryset(teachers, request)
    return render(request, "teacher_list.html", {
        "page_obj": page_obj,
        "teachers": page_obj.object_list,
        "query": query,
    })


@permission_required_custom("students.can_manage_teacher")
def teacher_create(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "教师已创建")
            return redirect("teacher_list")
    else:
        form = TeacherForm()
    return render(request, "teacher_form.html", {"form": form, "mode": "create"})


@permission_required_custom("students.can_manage_teacher")
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "教师已更新")
            return redirect("teacher_list")
    else:
        form = TeacherForm(instance=teacher)
    return render(request, "teacher_form.html", {"form": form, "mode": "update", "teacher": teacher})


@permission_required_custom("students.can_manage_teacher")
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        try:
            teacher.delete()
            messages.success(request, "教师已删除")
        except Exception:
            messages.error(request, "该教师有关联课程，无法删除")
    return redirect("teacher_list")


@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher.objects.select_related("department"), pk=pk)
    courses = teacher.courses.select_related("department").all()
    return render(request, "teacher_detail.html", {"teacher": teacher, "courses": courses})
