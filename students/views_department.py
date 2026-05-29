"""Department CRUD views."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import permission_required_custom
from .forms import DepartmentForm
from .models import Department
from .utils import paginate_queryset


@login_required
def department_list(request):
    query = (request.GET.get("q") or "").strip()
    departments = Department.objects.all()
    if query:
        departments = departments.filter(Q(name__icontains=query) | Q(code__icontains=query))
    page_obj = paginate_queryset(departments, request)
    return render(request, "department_list.html", {
        "page_obj": page_obj,
        "departments": page_obj.object_list,
        "query": query,
    })


@permission_required_custom("students.can_manage_department")
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "院系已创建")
            return redirect("department_list")
    else:
        form = DepartmentForm()
    return render(request, "department_form.html", {"form": form, "mode": "create"})


@permission_required_custom("students.can_manage_department")
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "院系已更新")
            return redirect("department_list")
    else:
        form = DepartmentForm(instance=department)
    return render(request, "department_form.html", {"form": form, "mode": "update", "department": department})


@permission_required_custom("students.can_manage_department")
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        try:
            department.delete()
            messages.success(request, "院系已删除")
        except Exception:
            messages.error(request, "该院系下还有班级或教师，无法删除")
    return redirect("department_list")
