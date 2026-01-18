from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Student


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "用户名",
            "password1": "密码",
            "password2": "确认密码",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "age",
            "major",
            "enrollment_date",
            "graduation_date",
        ]
        labels = {
            "student_id": "学号",
            "name": "姓名",
            "age": "年龄",
            "major": "专业名称",
            "enrollment_date": "入学时间",
            "graduation_date": "毕业时间",
        }
        widgets = {
            "enrollment_date": forms.DateInput(attrs={"type": "date"}),
            "graduation_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})
