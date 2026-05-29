from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models


# ──────────────────────────────────────────────
# 院系
# ──────────────────────────────────────────────
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="院系名称")
    code = models.CharField(max_length=10, unique=True, verbose_name="院系编码")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ["code"]
        verbose_name = "院系"
        verbose_name_plural = "院系"
        permissions = [
            ("can_manage_department", "可以管理院系"),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


# ──────────────────────────────────────────────
# 班级
# ──────────────────────────────────────────────
class ClassInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="班级名称")
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="classes",
        verbose_name="所属院系",
    )
    grade_year = models.PositiveIntegerField(verbose_name="入学年份")
    advisor = models.CharField(max_length=50, blank=True, default="", verbose_name="班主任")

    class Meta:
        ordering = ["department", "grade_year", "name"]
        unique_together = ("name", "department", "grade_year")
        verbose_name = "班级"
        verbose_name_plural = "班级"
        permissions = [
            ("can_manage_class", "可以管理班级"),
        ]

    def __str__(self):
        return f"{self.department.code}-{self.grade_year}级-{self.name}"


# ──────────────────────────────────────────────
# 教师
# ──────────────────────────────────────────────
class Teacher(models.Model):
    teacher_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(10)],
        verbose_name="工号",
    )
    name = models.CharField(max_length=50, verbose_name="姓名")
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="teachers",
        verbose_name="所属院系",
    )
    phone = models.CharField(max_length=20, blank=True, default="", verbose_name="电话")
    email = models.EmailField(blank=True, default="", verbose_name="邮箱")
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teacher_profile",
        verbose_name="关联用户",
    )

    class Meta:
        ordering = ["teacher_id"]
        verbose_name = "教师"
        verbose_name_plural = "教师"
        permissions = [
            ("can_manage_teacher", "可以管理教师"),
        ]

    def __str__(self):
        return f"{self.teacher_id} - {self.name}"


# ──────────────────────────────────────────────
# 学生
# ──────────────────────────────────────────────
class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
        verbose_name="学号",
    )
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="年龄",
    )
    major = models.CharField(max_length=100, verbose_name="专业名称")
    enrollment_date = models.DateField(verbose_name="入学时间")
    graduation_date = models.DateField(verbose_name="毕业时间")
    class_info = models.ForeignKey(
        ClassInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="班级",
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True,
        default="",
        verbose_name="头像",
    )

    class Meta:
        ordering = ["student_id"]
        verbose_name = "学生"
        verbose_name_plural = "学生"
        permissions = [
            ("can_manage_student", "可以管理学生"),
        ]

    def __str__(self):
        return f"{self.student_id} - {self.name}"


# ──────────────────────────────────────────────
# 课程
# ──────────────────────────────────────────────
class Course(models.Model):
    course_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="课程编号",
    )
    name = models.CharField(max_length=100, verbose_name="课程名称")
    credit = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="学分",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="授课教师",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="开课院系",
    )
    description = models.TextField(blank=True, default="", verbose_name="课程描述")
    max_students = models.PositiveIntegerField(default=60, verbose_name="最大学生数")

    class Meta:
        ordering = ["course_id"]
        verbose_name = "课程"
        verbose_name_plural = "课程"
        permissions = [
            ("can_manage_course", "可以管理课程"),
        ]

    def __str__(self):
        return f"{self.course_id} - {self.name}"


# ──────────────────────────────────────────────
# 选课 / 成绩
# ──────────────────────────────────────────────
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("enrolled", "在修"),
        ("dropped", "退选"),
        ("completed", "已完成"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="学生",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="课程",
    )
    semester = models.CharField(max_length=20, verbose_name="学期", help_text="如 2025-2026-1")
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="成绩",
    )
    grade_point = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="绩点",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="enrolled",
        verbose_name="状态",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="选课时间")

    class Meta:
        ordering = ["-semester", "student"]
        unique_together = ("student", "course", "semester")
        verbose_name = "选课记录"
        verbose_name_plural = "选课记录"
        permissions = [
            ("can_manage_grade", "可以管理成绩"),
        ]

    def save(self, *args, **kwargs):
        # Auto-calculate grade_point from score
        if self.score is not None:
            if self.score >= 90:
                self.grade_point = 4.0
            elif self.score >= 80:
                self.grade_point = 3.0
            elif self.score >= 70:
                self.grade_point = 2.0
            elif self.score >= 60:
                self.grade_point = 1.0
            else:
                self.grade_point = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} ({self.semester})"


# ──────────────────────────────────────────────
# 考勤
# ──────────────────────────────────────────────
class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "出勤"),
        ("late", "迟到"),
        ("absent", "缺勤"),
        ("leave", "请假"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="学生",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="课程",
    )
    date = models.DateField(verbose_name="日期")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present",
        verbose_name="状态",
    )
    remark = models.CharField(max_length=200, blank=True, default="", verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="记录时间")

    class Meta:
        ordering = ["-date", "student"]
        unique_together = ("student", "course", "date")
        verbose_name = "考勤记录"
        verbose_name_plural = "考勤记录"
        permissions = [
            ("can_manage_attendance", "可以管理考勤"),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.date} ({self.get_status_display()})"


# ──────────────────────────────────────────────
# 审计日志
# ──────────────────────────────────────────────
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("create", "创建"),
        ("update", "修改"),
        ("delete", "删除"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="操作用户",
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, verbose_name="操作")
    model_name = models.CharField(max_length=50, verbose_name="模型名称")
    object_id = models.CharField(max_length=50, verbose_name="对象ID")
    object_repr = models.CharField(max_length=200, verbose_name="对象描述")
    changes = models.TextField(
        blank=True,
        default="{}",
        verbose_name="变更内容 (JSON)",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP地址")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "审计日志"
        verbose_name_plural = "审计日志"

    def __str__(self):
        return f"[{self.get_action_display()}] {self.model_name} #{self.object_id} by {self.user}"
