"""PDF report generation."""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Enrollment, Student

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


@login_required
def student_report_pdf(request, pk):
    """Generate a PDF transcript for a student."""
    if not REPORTLAB_AVAILABLE:
        return HttpResponse("reportlab 未安装，无法生成 PDF", status=500)

    student = get_object_or_404(Student, pk=pk)
    enrollments = Enrollment.objects.filter(student=student).select_related("course")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="report_{student.student_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        "TitleCN", parent=styles["Title"], fontSize=18, spaceAfter=20
    )
    elements.append(Paragraph(f"成绩单 - {student.name}", title_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Student info
    info_data = [
        ["学号", student.student_id],
        ["姓名", student.name],
        ["专业", student.major],
        ["班级", str(student.class_info) if student.class_info else "-"],
    ]
    info_table = Table(info_data, colWidths=[4 * cm, 10 * cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 1 * cm))

    # Grades table
    elements.append(Paragraph("课程成绩", styles["Heading2"]))
    grade_data = [["课程编号", "课程名称", "学分", "成绩", "绩点", "学期"]]
    for e in enrollments:
        grade_data.append([
            e.course.course_id,
            e.course.name,
            str(e.course.credit),
            str(e.score) if e.score is not None else "-",
            str(e.grade_point) if e.grade_point is not None else "-",
            e.semester,
        ])

    grade_table = Table(grade_data, colWidths=[2.5 * cm, 4 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 3 * cm])
    grade_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(grade_table)

    doc.build(elements)
    return response
