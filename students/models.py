from django.core.validators import MaxValueValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.db import models


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

    class Meta:
        ordering = ["student_id"]
        verbose_name = "学生"
        verbose_name_plural = "学生"

    def __str__(self) -> str:
        return f"{self.student_id} - {self.name}"
