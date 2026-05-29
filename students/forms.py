from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from .models import (
    Attendance,
    ClassInfo,
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
)


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

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Auto-assign student_viewer role
        student_group, _ = Group.objects.get_or_create(name="student_viewer")
        user.groups.add(student_group)
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "name",
            "age",
            "major",
            "class_info",
            "enrollment_date",
            "graduation_date",
        ]
        labels = {
            "student_id": "学号",
            "name": "姓名",
            "age": "年龄",
            "major": "专业名称",
            "class_info": "班级",
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

    def clean(self):
        cleaned_data = super().clean()
        enrollment = cleaned_data.get("enrollment_date")
        graduation = cleaned_data.get("graduation_date")
        if enrollment and graduation and enrollment >= graduation:
            raise forms.ValidationError("入学时间必须早于毕业时间")
        return cleaned_data


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "code", "description"]
        labels = {"name": "院系名称", "code": "院系编码", "description": "描述"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})


class ClassInfoForm(forms.ModelForm):
    class Meta:
        model = ClassInfo
        fields = ["name", "department", "grade_year", "advisor"]
        labels = {
            "name": "班级名称",
            "department": "所属院系",
            "grade_year": "入学年份",
            "advisor": "班主任",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["teacher_id", "name", "department", "phone", "email"]
        labels = {
            "teacher_id": "工号",
            "name": "姓名",
            "department": "所属院系",
            "phone": "电话",
            "email": "邮箱",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_id", "name", "credit", "teacher", "department", "description", "max_students"]
        labels = {
            "course_id": "课程编号",
            "name": "课程名称",
            "credit": "学分",
            "teacher": "授课教师",
            "department": "开课院系",
            "description": "课程描述",
            "max_students": "最大学生数",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student", "course", "semester", "score", "status"]
        labels = {
            "student": "学生",
            "course": "课程",
            "semester": "学期",
            "score": "成绩",
            "status": "状态",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})

    def clean_score(self):
        score = self.cleaned_data.get("score")
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError("成绩必须在 0-100 之间")
        return score


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["student", "course", "date", "status", "remark"]
        labels = {
            "student": "学生",
            "course": "课程",
            "date": "日期",
            "status": "状态",
            "remark": "备注",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs.update({"class": f"form-control {existing}".strip()})
