"""Seed database with demo data."""

import random
from datetime import date, timedelta

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from students.models import (
    Attendance,
    ClassInfo,
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
)

FIRST_NAMES = ["张", "李", "王", "刘", "陈", "杨", "黄", "赵", "周", "吴"]
LAST_NAMES = ["伟", "芳", "秀英", "敏", "静", "丽", "强", "磊", "洋", "勇", "艳", "杰", "娜", "军", "超"]


class Command(BaseCommand):
    help = "填充演示数据并创建角色组"

    def handle(self, *args, **options):
        self.stdout.write("创建角色组...")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        teacher_group, _ = Group.objects.get_or_create(name="teacher")
        student_group, _ = Group.objects.get_or_create(name="student_viewer")

        # Create admin user
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser("admin", "admin@example.com", "admin123")
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS("  管理员 admin / admin123"))

        # Departments
        self.stdout.write("创建院系...")
        dept_data = [
            ("CS", "计算机科学与技术学院", "涵盖软件工程、人工智能等方向"),
            ("MATH", "数学与统计学院", "涵盖应用数学、统计学等方向"),
            ("FL", "外国语学院", "涵盖英语、日语等方向"),
        ]
        departments = []
        for code, name, desc in dept_data:
            dept, _ = Department.objects.get_or_create(code=code, defaults={"name": name, "description": desc})
            departments.append(dept)

        # Classes
        self.stdout.write("创建班级...")
        classes = []
        for dept in departments:
            for year in [2023, 2024]:
                cls, _ = ClassInfo.objects.get_or_create(
                    name=f"{dept.code}{year % 100}01",
                    department=dept,
                    grade_year=year,
                    defaults={"advisor": random.choice(FIRST_NAMES) + random.choice(LAST_NAMES)},
                )
                classes.append(cls)

        # Teachers
        self.stdout.write("创建教师...")
        teachers = []
        for i, dept in enumerate(departments):
            for j in range(2):
                tid = f"T{dept.code}{j+1:03d}"
                name = random.choice(FIRST_NAMES) + random.choice(LAST_NAMES)
                teacher, _ = Teacher.objects.get_or_create(
                    teacher_id=tid,
                    defaults={
                        "name": name,
                        "department": dept,
                        "phone": f"138{random.randint(10000000, 99999999)}",
                        "email": f"{tid.lower()}@example.com",
                    },
                )
                teachers.append(teacher)

        # Courses
        self.stdout.write("创建课程...")
        course_templates = {
            "CS": [
                ("CS101", "程序设计基础", 4),
                ("CS201", "数据结构与算法", 4),
                ("CS301", "数据库原理", 3),
                ("CS401", "人工智能导论", 3),
            ],
            "MATH": [
                ("MATH101", "高等数学", 5),
                ("MATH201", "线性代数", 3),
                ("MATH301", "概率论与数理统计", 3),
            ],
            "FL": [
                ("FL101", "大学英语", 4),
                ("FL201", "英语听说", 2),
                ("FL301", "日语入门", 3),
            ],
        }
        courses = []
        for dept in departments:
            dept_courses = course_templates.get(dept.code, [])
            dept_teachers = [t for t in teachers if t.department == dept]
            for cid, cname, credit in dept_courses:
                course, _ = Course.objects.get_or_create(
                    course_id=cid,
                    defaults={
                        "name": cname,
                        "credit": credit,
                        "teacher": random.choice(dept_teachers) if dept_teachers else None,
                        "department": dept,
                    },
                )
                courses.append(course)

        # Students
        self.stdout.write("创建学生...")
        students = []
        for cls in classes:
            for k in range(5):
                sid = f"{cls.grade_year}{cls.department.code}{k+1:04d}"
                sid = sid[:10].ljust(10, "0")
                name = random.choice(FIRST_NAMES) + random.choice(LAST_NAMES)
                age = random.randint(18, 24)
                enroll_date = date(cls.grade_year, 9, 1)
                grad_date = date(cls.grade_year + 4, 6, 30)
                student, _ = Student.objects.get_or_create(
                    student_id=sid,
                    defaults={
                        "name": name,
                        "age": age,
                        "major": cls.department.name.replace("学院", ""),
                        "enrollment_date": enroll_date,
                        "graduation_date": grad_date,
                        "class_info": cls,
                    },
                )
                students.append(student)

        # Enrollments (random)
        self.stdout.write("创建选课记录...")
        semesters = ["2024-2025-1", "2024-2025-2"]
        for student in students:
            dept_courses = [c for c in courses if c.department == student.class_info.department]
            chosen = random.sample(dept_courses, min(3, len(dept_courses)))
            for course in chosen:
                semester = random.choice(semesters)
                score = round(random.uniform(45, 100), 1) if random.random() > 0.2 else None
                Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    semester=semester,
                    defaults={
                        "score": score,
                        "status": "completed" if score else "enrolled",
                    },
                )

        # Attendance (sample)
        self.stdout.write("创建考勤记录...")
        statuses = ["present"] * 7 + ["late", "absent", "leave"]
        for student in students[:20]:
            dept_courses = [c for c in courses if c.department == student.class_info.department]
            if dept_courses:
                course = random.choice(dept_courses)
                for day_offset in range(10):
                    att_date = date.today() - timedelta(days=day_offset * 7)
                    Attendance.objects.get_or_create(
                        student=student,
                        course=course,
                        date=att_date,
                        defaults={"status": random.choice(statuses)},
                    )

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ 演示数据创建完成！\n"
            f"   院系: {Department.objects.count()}\n"
            f"   班级: {ClassInfo.objects.count()}\n"
            f"   教师: {Teacher.objects.count()}\n"
            f"   课程: {Course.objects.count()}\n"
            f"   学生: {Student.objects.count()}\n"
            f"   选课: {Enrollment.objects.count()}\n"
            f"   考勤: {Attendance.objects.count()}\n"
            f"   管理员: admin / admin123"
        ))
