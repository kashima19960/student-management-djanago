"""ClassInfo CRUD views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .forms import ClassInfoForm
from .models import ClassInfo, Department
from .utils import paginate_queryset


@login_required
def class_list(request):
    query = (request.GET.get("q") or "").strip()
    dept_id = request.GET.get("department", "")
    classes = ClassInfo.objects.select_related("department").all()
    if query:
        classes = classes.filter(Q(name__icontains=query))
    if dept_id:
        classes = classes.filter(department_id=dept_id)
    departments = Department.objects.all()
    page_obj = paginate_queryset(classes, request)
    return render(request, "class_list.html", {
        "page_obj": page_obj,
        "classes": page_obj.object_list,
        "query": query,
        "departments": departments,
        "selected_dept": dept_id,
    })


@permission_required_custom("students.can_manage_class")
def class_create(request):
    if request.method == "POST":
        form = ClassInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "班级已创建")
            return redirect("class_list")
    else:
        form = ClassInfoForm()
    return render(request, "class_form.html", {"form": form, "mode": "create"})


@permission_required_custom("students.can_manage_class")
def class_update(request, pk):
    cls = get_object_or_404(ClassInfo, pk=pk)
    if request.method == "POST":
        form = ClassInfoForm(request.POST, instance=cls)
        if form.is_valid():
            form.save()
            messages.success(request, "班级已更新")
            return redirect("class_list")
    else:
        form = ClassInfoForm(instance=cls)
    return render(request, "class_form.html", {"form": form, "mode": "update", "class_info": cls})


@permission_required_custom("students.can_manage_class")
def class_delete(request, pk):
    cls = get_object_or_404(ClassInfo, pk=pk)
    if request.method == "POST":
        try:
            cls.delete()
            messages.success(request, "班级已删除")
        except Exception:
            messages.error(request, "该班级下还有学生，无法删除")
    return redirect("class_list")


@login_required
def class_detail(request, pk):
    cls = get_object_or_404(ClassInfo.objects.select_related("department"), pk=pk)
    students = cls.students.all()
    return render(request, "class_detail.html", {"class_info": cls, "students": students})
