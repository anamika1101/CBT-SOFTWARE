from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import require_role
from companylogin.models import Center, Test
from .models import CenterStudent, ExamAssignment


def _get_logged_center(request):
    center_id = request.session.get("center_id")
    return get_object_or_404(Center, id=center_id)


@require_role("center")
def cendashboard(request):
    center = _get_logged_center(request)
    students = CenterStudent.objects.filter(center=center)
    tests = Test.objects.all().order_by("test_name")
    assignments = ExamAssignment.objects.filter(center=center).select_related("student", "test")

    completed = assignments.filter(status="COMPLETED")
    passed = sum(1 for row in completed if row.score * 2 >= row.test.total_marks)
    pass_rate = int((passed / completed.count()) * 100) if completed.exists() else 0

    avg_score = int(sum(row.score for row in completed) / completed.count()) if completed.exists() else 0

    result_rows = [
        {
            "assignment": row,
            "is_pass": row.score * 2 >= row.test.total_marks,
        }
        for row in completed
    ]

    context = {
        "center": center,
        "students": students,
        "tests": tests,
        "assignments": assignments,
        "monitor_rows": assignments.exclude(status="COMPLETED"),
        "result_rows": result_rows,
        "stats": {
            "students": students.count(),
            "active_exams": assignments.filter(status__in=["ASSIGNED", "IN_PROGRESS"]).count(),
            "conducted": completed.count(),
            "pass_rate": pass_rate,
        },
        "report": {
            "total_assigned": assignments.count(),
            "total_completed": completed.count(),
            "total_in_progress": assignments.filter(status="IN_PROGRESS").count(),
            "avg_score": avg_score,
        },
    }
    return render(request, "cen_dashboard_modern.html", context)


@require_role("center")
def add_student(request):
    if request.method != "POST":
        return redirect("cendashboard")

    center = _get_logged_center(request)
    roll_no = request.POST.get("roll_no", "").strip()
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    course = request.POST.get("course", "").strip()

    if not all([roll_no, name, email, phone]):
        messages.error(request, "Roll no, name, email and phone are required.")
        return redirect("cendashboard")

    if CenterStudent.objects.filter(center=center, roll_no=roll_no).exists():
        messages.error(request, "Student roll number already exists.")
        return redirect("cendashboard")

    CenterStudent.objects.create(
        center=center,
        roll_no=roll_no,
        name=name,
        email=email,
        phone=phone,
        course=course,
    )
    messages.success(request, "Student registered successfully.")
    return redirect("cendashboard")


@require_role("center")
def edit_student(request, student_id):
    if request.method != "POST":
        return redirect("cendashboard")

    center = _get_logged_center(request)
    student = get_object_or_404(CenterStudent, id=student_id, center=center)

    student.name = request.POST.get("name", student.name).strip()
    student.email = request.POST.get("email", student.email).strip()
    student.phone = request.POST.get("phone", student.phone).strip()
    student.course = request.POST.get("course", student.course).strip()
    status = request.POST.get("status", student.status)
    student.status = status if status in {"ACTIVE", "INACTIVE"} else student.status
    student.save()

    messages.success(request, "Student updated successfully.")
    return redirect("cendashboard")


@require_role("center")
def delete_student(request, student_id):
    if request.method != "POST":
        return redirect("cendashboard")

    center = _get_logged_center(request)
    student = get_object_or_404(CenterStudent, id=student_id, center=center)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("cendashboard")


@require_role("center")
def assign_exam(request):
    if request.method != "POST":
        return redirect("cendashboard")

    center = _get_logged_center(request)
    student_id = request.POST.get("student_id")
    test_id = request.POST.get("test_id")

    student = get_object_or_404(CenterStudent, id=student_id, center=center)
    test = get_object_or_404(Test, id=test_id)

    assignment, created = ExamAssignment.objects.get_or_create(
        center=center,
        student=student,
        test=test,
    )

    if created:
        messages.success(request, "Exam assigned successfully.")
    else:
        messages.info(request, "Exam already assigned to this student.")
    return redirect("cendashboard")


@require_role("center")
def update_assignment(request, assignment_id):
    if request.method != "POST":
        return redirect("cendashboard")

    center = _get_logged_center(request)
    assignment = get_object_or_404(ExamAssignment, id=assignment_id, center=center)
    action = request.POST.get("action_type")

    if action == "start" and assignment.status == "ASSIGNED":
        assignment.status = "IN_PROGRESS"
        assignment.started_at = timezone.now()
        assignment.save()
        messages.success(request, "Exam monitoring started.")

    elif action == "complete":
        try:
            score = int(request.POST.get("score", assignment.score))
        except (TypeError, ValueError):
            score = assignment.score

        assignment.status = "COMPLETED"
        assignment.score = max(0, min(score, assignment.test.total_marks))
        if assignment.started_at is None:
            assignment.started_at = timezone.now()
        assignment.ended_at = timezone.now()
        assignment.save()
        messages.success(request, "Exam marked as completed and result saved.")

    return redirect("cendashboard")


@require_role("center")
def cenlogout(request):
    if request.session.get("center_id"):
        del request.session["center_id"]
    return redirect("homepage")


@require_role("center")
def entrylogin(request):
    return render(request, "cen_entrylogin.html")


@require_role("center")
def studentlist(request):
    return render(request, "studentlist.html")


@require_role("center")
def democenter(request):
    return render(request, "democenter.html")


@require_role("center")
def emergency(request):
    return render(request, "cen_emer.html")


@require_role("center")
def seatarr(request):
    return render(request, "seat_arrange.html")
