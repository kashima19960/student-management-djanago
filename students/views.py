from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, StudentForm
from .models import Student


def _apply_bootstrap(form):
    if "username" in form.fields:
        form.fields["username"].label = "用户名"
    if "password" in form.fields:
        form.fields["password"].label = "密码"
    for field in form.fields.values():
        existing = field.widget.attrs.get("class", "")
        field.widget.attrs.update({"class": f"form-control {existing}".strip()})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功，欢迎使用学生管理系统！")
            return redirect("student_list")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        _apply_bootstrap(form)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "登录成功")
            next_url = request.GET.get("next") or "student_list"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)
        _apply_bootstrap(form)

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def student_list(request):
    query = (request.GET.get("q") or "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(Q(student_id=query) | Q(name__icontains=query))
    context = {
        "students": students,
        "query": query,
    }
    return render(request, "student_list.html", context)


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "学生信息已创建")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "student_form.html", {"form": form, "mode": "create"})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "学生信息已更新")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "student_form.html", {"form": form, "mode": "update", "student": student})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "学生信息已删除")
    return redirect("student_list")
